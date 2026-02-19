from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from db.car_model import CarStatus
from db.rental_model import Rental
from services.interfaces.rental_service_interface import IRentalService
from repositories.interfaces.rental_repository_interface import IRentalRepository
from repositories.interfaces.car_repository_interface import ICarRepository
from fastapi import HTTPException, status

class RentalService(IRentalService):
    def __init__(self, rental_repository: IRentalRepository, car_repository: ICarRepository):
        self.rental_repository = rental_repository
        self.car_repository = car_repository

    def get_all_rentals(self) -> List[Rental]:
        return self.rental_repository.get_all()

    def create_rental(self, car_id: UUID, customer_name: str) -> Rental:
        car = self.car_repository.get_by_id(car_id)
        
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
        
        if car.status != CarStatus.AVAILABLE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Car is not available for rent")

        new_rental = self.rental_repository.create(car_id=car_id, customer_name=customer_name)
        car.status = CarStatus.IN_USE
        self.car_repository.update(car)

        return new_rental

    def end_rental(self, rental_id: UUID) -> Rental:
        rental = self.rental_repository.get_by_id(rental_id)
        if not rental:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rental not found")
        
        if rental.end_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rental already ended")

        self.rental_repository.end_rental(rental)
        
        car = self.car_repository.get_by_id(rental.car_id)
        if car:
            car.status = CarStatus.AVAILABLE
            self.car_repository.update(car)
            
        return rental
