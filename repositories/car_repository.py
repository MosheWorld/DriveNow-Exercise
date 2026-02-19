from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from db.car_model import Car, CarStatus

class CarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Car]:
        return self.db.query(Car).all()

    def get_by_id(self, car_id: UUID) -> Optional[Car]:
        return self.db.query(Car).filter(Car.id == car_id).first()

    def create(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> Car:
        car = Car(model=model, year=year, status=status)
        self.db.add(car)
        self.db.commit()
        self.db.refresh(car)
        return car
