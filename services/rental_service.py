from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from db.car_model import CarStatus
from db.rental_model import Rental
from repositories.rental_repository import RentalRepository
from repositories.car_repository import CarRepository
from fastapi import HTTPException, status

class RentalService:
    def __init__(self, db: Session):
        self.rental_repository = RentalRepository(db)
        self.car_repository = CarRepository(db)

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
        self.car_repository.db.commit()
        
        return new_rental
