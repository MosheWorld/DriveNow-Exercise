from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from db.car_model import Car, CarStatus
from datetime import datetime, timezone

from repositories.interfaces.car_repository_interface import ICarRepository
from common.exceptions import DatabaseException

class CarRepository(ICarRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self, status: Optional[CarStatus] = None) -> List[Car]:
        try:
            query = select(Car)
            if status:
                query = query.filter(Car.status == status)
            result = await self.db.execute(query)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving cars: {e}", original_exception=e)

    async def get_by_id(self, car_id: UUID) -> Optional[Car]:
        try:
            result = await self.db.execute(select(Car).filter(Car.id == car_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving car by ID {car_id}: {e}", original_exception=e)

    async def create(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> Car:
        try:
            car = Car(model=model, year=year, status=status)
            self.db.add(car)
            await self.db.commit()
            await self.db.refresh(car)
            return car
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error creating car: {e}", original_exception=e)

    async def update(self, car: Car) -> Car:
        try:
            car.updated_at = datetime.now(timezone.utc)
            self.db.add(car)
            await self.db.commit()
            await self.db.refresh(car)
            return car
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error updating car {car.id}: {e}", original_exception=e)
