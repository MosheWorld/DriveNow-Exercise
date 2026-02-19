from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from db.car_model import Car, CarStatus
from datetime import datetime, timezone

class CarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, status: Optional[CarStatus] = None) -> List[Car]:
        query = self.db.query(Car)
        if status:
            query = query.filter(Car.status == status)
        return query.all()

    def get_by_id(self, car_id: UUID) -> Optional[Car]:
        return self.db.query(Car).filter(Car.id == car_id).first()

    def create(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> Car:
        car = Car(model=model, year=year, status=status)
        self.db.add(car)
        self.db.commit()
        self.db.refresh(car)
        return car

    def update(self, car: Car) -> Car:
        car.updated_at = datetime.now(timezone.utc)
        self.db.add(car)
        self.db.commit()
        self.db.refresh(car)
        return car
