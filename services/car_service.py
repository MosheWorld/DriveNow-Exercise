from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from db.car_model import CarStatus, Car
from repositories.car_repository import CarRepository

class CarService:
    def __init__(self, db: Session):
        self.repository = CarRepository(db)

    def get_all_cars(self, status: Optional[CarStatus] = None) -> List[Car]:
        return self.repository.get_all(status)

    def get_car_by_id(self, car_id: UUID) -> Optional[Car]:
        return self.repository.get_by_id(car_id)

    def create_car(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> Car:
        return self.repository.create(model=model, year=year, status=status)

    def update_car(self, car_id: UUID, model: Optional[str] = None, year: Optional[int] = None, status: Optional[CarStatus] = None) -> Optional[Car]:
        car = self.repository.get_by_id(car_id)
        if not car:
            return None
            
        if model:
            car.model = model
        if year:
            car.year = year
        if status:
            car.status = status
            
        return self.repository.update(car)
