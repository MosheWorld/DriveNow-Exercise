from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.car_model import Car, CarStatus
from datetime import datetime, timezone

from repositories.interfaces.car_repository_interface import ICarRepository
from api.common.exceptions import DatabaseException

class CarRepository(ICarRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, status: Optional[CarStatus] = None) -> List[Car]:
        try:
            query = self.db.query(Car)
            if status:
                query = query.filter(Car.status == status)
            return query.all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving cars: {e}", original_exception=e)

    def get_by_id(self, car_id: UUID) -> Optional[Car]:
        try:
            return self.db.query(Car).filter(Car.id == car_id).first()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving car by ID {car_id}: {e}", original_exception=e)

    def create(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> Car:
        try:
            car = Car(model=model, year=year, status=status)
            self.db.add(car)
            self.db.commit()
            self.db.refresh(car)
            return car
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(f"Error creating car: {e}", original_exception=e)

    def update(self, car: Car) -> Car:
        try:
            car.updated_at = datetime.now(timezone.utc)
            self.db.add(car)
            self.db.commit()
            self.db.refresh(car)
            return car
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(f"Error updating car {car.id}: {e}", original_exception=e)
