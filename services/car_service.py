from typing import List, Optional
from uuid import UUID
from db.car_model import CarStatus, Car
from services.interfaces.car_service_interface import ICarService
from repositories.interfaces.car_repository_interface import ICarRepository
from common.exceptions import NotFoundException, InputValidationException
from common.interfaces.logger_interface import ILogger
from common.interfaces.message_publisher_interface import IMessagePublisher
import common.messaging.messaging_constants as constants

MIN_CAR_YEAR = 1950

class CarService(ICarService):
    def __init__(self, logger: ILogger, message_publisher: IMessagePublisher, repository: ICarRepository) -> None:
        self.logger = logger
        self.message_publisher = message_publisher
        self.repository = repository

    def get_all_cars(self, status: Optional[CarStatus] = None) -> List[Car]:
        return self.repository.get_all(status)

    def create_car(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> Car:
        self.logger.info(f"Creating car: {model} ({year})")
        if not model or not model.strip():
            self.logger.error("Attempted to create car with empty model")
            raise InputValidationException("Car model cannot be empty")
        
        if year < MIN_CAR_YEAR:
            self.logger.error(f"Attempted to create car with year {year} < {MIN_CAR_YEAR}")
            raise InputValidationException(f"Car year must be {MIN_CAR_YEAR} or later")
            
        created_car = self.repository.create(model=model, year=year, status=status)
        self._update_car_metrics_on_create(status)
        self.logger.info(f"Car created successfully: {created_car.id}")
        return created_car

    def _update_car_metrics_on_create(self, status: CarStatus) -> None:
        if status == CarStatus.AVAILABLE:
            self.message_publisher.publish_event(constants.EVENT_CAR_CREATED_AVAILABLE, {})

    def update_car(self, car_id: UUID, model: Optional[str] = None, year: Optional[int] = None, status: Optional[CarStatus] = None) -> Optional[Car]:
        self.logger.info(f"Updating car: {car_id}")
        if model is not None and not model.strip():
             self.logger.error("Attempted to update car with empty model")
             raise InputValidationException("Car model cannot be empty")
             
        if year is not None and year < MIN_CAR_YEAR:
            self.logger.error(f"Attempted to update car with year {year} < {MIN_CAR_YEAR}")
            raise InputValidationException(f"Car year must be {MIN_CAR_YEAR} or later")

        car = self.repository.get_by_id(car_id)
        if not car:
            self.logger.error(f"Car {car_id} not found for update")
            raise NotFoundException(f"Car {car_id} not found")
            
        old_status = car.status
        self._update_car_attributes(car, model, year, status)
        updated_car = self.repository.update(car)
        self._update_car_metrics_on_update(old_status, status)

        self.logger.info(f"Car updated successfully: {updated_car.id}")
        return updated_car

    def _update_car_attributes(self, car: Car, model: Optional[str], year: Optional[int], status: Optional[CarStatus]) -> None:
        if model:
            car.model = model
        if year:
            car.year = year
        if status:
            car.status = status

    def _update_car_metrics_on_update(self, old_status: CarStatus, new_status: Optional[CarStatus]) -> None:
        if new_status is None or old_status == new_status:
            return
            
        if old_status == CarStatus.AVAILABLE and new_status != CarStatus.AVAILABLE:
            self.message_publisher.publish_event(constants.EVENT_CAR_STATUS_CHANGED_FROM_AVAILABLE, {})
        elif old_status != CarStatus.AVAILABLE and new_status == CarStatus.AVAILABLE:
            self.message_publisher.publish_event(constants.EVENT_CAR_STATUS_CHANGED_TO_AVAILABLE, {})
