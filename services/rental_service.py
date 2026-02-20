from typing import List
from uuid import UUID
from domain.entities.car import CarStatus
from domain.entities.rental import RentalEntity
from services.interfaces.rental_service_interface import IRentalService
from repositories.interfaces.rental_repository_interface import IRentalRepository
from repositories.interfaces.car_repository_interface import ICarRepository
from common.exceptions import NotFoundException, CarStatusUnavailableException, RentalAlreadyEndedException, InputValidationException
from common.interfaces.logger_interface import ILogger
from common.interfaces.message_publisher_interface import IMessagePublisher
import common.messaging.messaging_constants as constants

class RentalService(IRentalService):
    def __init__(self, logger: ILogger, message_publisher: IMessagePublisher, rental_repository: IRentalRepository, car_repository: ICarRepository) -> None:
        self.logger = logger
        self.message_publisher = message_publisher
        self.rental_repository = rental_repository
        self.car_repository = car_repository

    async def get_all_rentals(self) -> List[RentalEntity]:
        return await self.rental_repository.get_all()

    async def create_rental(self, car_id: UUID, customer_name: str) -> RentalEntity:
        self.logger.info(f"Creating rental for car {car_id} by {customer_name}")
        if not customer_name or not customer_name.strip():
            self.logger.error("Attempted to create rental with empty customer name")
            raise InputValidationException(message="Customer name cannot be empty")

        car = await self.car_repository.get_by_id(car_id)
        if not car:
            self.logger.error(f"Car {car_id} not found during rental creation")
            raise NotFoundException(f"Car {car_id} not found")
        
        if car.status != CarStatus.AVAILABLE:
            self.logger.error(f"Car {car_id} is not available for rent (Status: {car.status})")
            raise CarStatusUnavailableException("Car is not available for rent")

        new_rental = await self.rental_repository.create(car_id=car_id, customer_name=customer_name)
        car.status = CarStatus.IN_USE
        await self.car_repository.update(car)
        
        await self.message_publisher.publish_event(constants.EVENT_RENTAL_CREATED, {"car_id": str(car_id), "rental_id": str(new_rental.id)})
        
        self.logger.info(f"Rental created successfully: {new_rental.id}")
        return new_rental

    async def end_rental_by_car_id(self, car_id: UUID) -> RentalEntity:
        self.logger.info(f"Ending rental for car: {car_id}")
        car = await self.car_repository.get_by_id(car_id)
        if not car:
            self.logger.error(f"Car {car_id} not found during end rental")
            raise NotFoundException(f"Car {car_id} not found")

        active_rental = await self.rental_repository.get_active_rental_by_car_id(car_id)
        if not active_rental:
            self.logger.error(f"No active rental found for car {car_id}")
            raise NotFoundException(f"No active rental found for car {car_id}")

        if active_rental.end_date:
            self.logger.error(f"Rental {active_rental.id} already ended")
            raise RentalAlreadyEndedException("Rental already ended")

        await self.rental_repository.end_rental(active_rental)
        
        car.status = CarStatus.AVAILABLE
        await self.car_repository.update(car)
        
        await self.message_publisher.publish_event(constants.EVENT_RENTAL_ENDED, {"car_id": str(car_id), "rental_id": str(active_rental.id)})
        
        self.logger.info(f"Rental ended successfully: {active_rental.id} for car {car_id}")
        return active_rental
