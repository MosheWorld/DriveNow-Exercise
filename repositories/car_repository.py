from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from db.car_model import Car as CarModel
from domain.entities.car import CarEntity, CarStatus
from datetime import datetime, timezone

from repositories.interfaces.car_repository_interface import ICarRepository
from common.exceptions import DatabaseException

def _to_entity(model: CarModel) -> CarEntity:
    return CarEntity(
        id=model.id,
        model=model.model,
        year=model.year,
        status=model.status,
        created_at=model.created_at,
        updated_at=model.updated_at
    )

class CarRepository(ICarRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self, status: Optional[CarStatus] = None) -> List[CarEntity]:
        try:
            query = select(CarModel)
            if status:
                query = query.filter(CarModel.status == status)
            result = await self.db.execute(query)
            return [_to_entity(car) for car in result.scalars().all()]
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving cars: {e}", original_exception=e)

    async def get_by_id(self, car_id: UUID) -> Optional[CarEntity]:
        try:
            query = select(CarModel).filter(CarModel.id == car_id)
            result = await self.db.execute(query)
            model = result.scalars().first()
            return _to_entity(model) if model else None
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving car by ID {car_id}: {e}", original_exception=e)

    async def create(self, model: str, year: int) -> CarEntity:
        try:
            car_model = CarModel(model=model, year=year, status=CarStatus.AVAILABLE)
            self.db.add(car_model)
            await self.db.commit()
            await self.db.refresh(car_model)
            return _to_entity(car_model)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error creating car: {e}", original_exception=e)

    async def update(self, car: CarEntity) -> CarEntity:
        try:
            car.updated_at = datetime.now(timezone.utc)
            db_car = CarModel(
                id=car.id,
                model=car.model,
                year=car.year,
                status=car.status,
                created_at=car.created_at,
                updated_at=car.updated_at
            )
            db_car = await self.db.merge(db_car)
            await self.db.commit()
            return _to_entity(db_car)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error updating car {car.id}: {e}", original_exception=e)
