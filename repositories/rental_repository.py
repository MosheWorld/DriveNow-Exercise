from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from db.rental_model import Rental

from repositories.interfaces.rental_repository_interface import IRentalRepository
from common.exceptions import DatabaseException

class RentalRepository(IRentalRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> List[Rental]:
        try:
            result = await self.db.execute(select(Rental))
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving rentals: {e}", original_exception=e)

    async def create(self, car_id: UUID, customer_name: str) -> Rental:
        try:
            rental = Rental(car_id=car_id, customer_name=customer_name)
            self.db.add(rental)
            await self.db.commit()
            await self.db.refresh(rental)
            return rental
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error creating rental: {e}", original_exception=e)

    async def end_rental(self, rental: Rental) -> Rental:
        try:
            rental.end_date = datetime.now(timezone.utc)
            rental.updated_at = datetime.now(timezone.utc)
            self.db.add(rental)
            await self.db.commit()
            await self.db.refresh(rental)
            return rental
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise DatabaseException(f"Error ending rental {rental.id}: {e}", original_exception=e)

    async def get_active_rental_by_car_id(self, car_id: UUID) -> Optional[Rental]:
        try:
            result = await self.db.execute(select(Rental).filter(Rental.car_id == car_id, Rental.end_date == None))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving active rental for car {car_id}: {e}", original_exception=e)
