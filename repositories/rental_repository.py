from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from db.rental_model import Rental as RentalModel
from domain.entities.rental import RentalEntity

from repositories.interfaces.rental_repository_interface import IRentalRepository
from common.exceptions import DatabaseException

def _to_entity(model: RentalModel) -> RentalEntity:
    return RentalEntity(
        id=model.id,
        car_id=model.car_id,
        customer_name=model.customer_name,
        start_date=model.start_date,
        end_date=model.end_date,
        created_at=model.created_at,
        updated_at=model.updated_at
    )

class RentalRepository(IRentalRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> List[RentalEntity]:
        try:
            result = await self.db.execute(select(RentalModel))
            return [_to_entity(rental_model) for rental_model in result.scalars().all()]
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving rentals: {e}", original_exception=e)

    async def create(self, car_id: UUID, customer_name: str) -> RentalEntity:
        try:
            rental = RentalModel(car_id=car_id, customer_name=customer_name)
            self.db.add(rental)
            await self.db.commit()
            await self.db.refresh(rental)
            return _to_entity(rental)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error creating rental: {e}", original_exception=e)

    async def end_rental(self, rental: RentalEntity) -> RentalEntity:
        try:
            rental.end_date = datetime.now(timezone.utc)
            rental.updated_at = datetime.now(timezone.utc)
            db_rental = RentalModel(
                id=rental.id,
                car_id=rental.car_id,
                customer_name=rental.customer_name,
                start_date=rental.start_date,
                end_date=rental.end_date,
                created_at=rental.created_at,
                updated_at=rental.updated_at
            )
            db_rental = await self.db.merge(db_rental)
            await self.db.commit()
            return _to_entity(db_rental)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error ending rental {rental.id}: {e}", original_exception=e)

    async def get_active_rental_by_car_id(self, car_id: UUID) -> Optional[RentalEntity]:
        try:
            query = select(RentalModel).filter(RentalModel.car_id == car_id, RentalModel.end_date == None)
            result = await self.db.execute(query)
            model = result.scalars().first()
            return _to_entity(model) if model else None
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving active rental for car {car_id}: {e}", original_exception=e)
