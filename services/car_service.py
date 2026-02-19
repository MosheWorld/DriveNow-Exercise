from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from db.car_model import CarStatus, Car
from services.interfaces.car_service_interface import ICarService
from repositories.interfaces.car_repository_interface import ICarRepository
from common.exceptions import NotFoundException, InputValidationException

MIN_CAR_YEAR = 1950

class CarService(ICarService):
    def __init__(self, repository: ICarRepository):
        self.repository = repository

    def get_all_cars(self, status: Optional[CarStatus] = None) -> List[Car]:
        return self.repository.get_all(status)

    def get_car_by_id(self, car_id: UUID) -> Optional[Car]:
        return self.repository.get_by_id(car_id)

    def create_car(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> Car:
        if not model or not model.strip():
            raise InputValidationException("Car model cannot be empty")
        
        if year < MIN_CAR_YEAR:
            raise InputValidationException(f"Car year must be {MIN_CAR_YEAR} or later")
            
        return self.repository.create(model=model, year=year, status=status)

    def update_car(self, car_id: UUID, model: Optional[str] = None, year: Optional[int] = None, status: Optional[CarStatus] = None) -> Optional[Car]:
        if model is not None and not model.strip():
             raise InputValidationException("Car model cannot be empty")
             
        if year is not None and year < MIN_CAR_YEAR:
            raise InputValidationException(f"Car year must be {MIN_CAR_YEAR} or later")

        car = self.repository.get_by_id(car_id)
        if not car:
            raise NotFoundException(f"Car {car_id} not found")
            
        if model:
            car.model = model
        if year:
            car.year = year
        if status:
            car.status = status
            
        return self.repository.update(car)
