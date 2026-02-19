from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.rental_model import Rental

from repositories.interfaces.rental_repository_interface import IRentalRepository
from api.common.exceptions import DatabaseException

class RentalRepository(IRentalRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Rental]:
        try:
            return self.db.query(Rental).all()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving rentals: {e}", original_exception=e)

    def get_by_id(self, rental_id: UUID) -> Optional[Rental]:
        try:
            return self.db.query(Rental).filter(Rental.id == rental_id).first()
        except SQLAlchemyError as e:
            raise DatabaseException(f"Error retrieving rental by ID {rental_id}: {e}", original_exception=e)

    def create(self, car_id: UUID, customer_name: str) -> Rental:
        try:
            rental = Rental(car_id=car_id, customer_name=customer_name)
            self.db.add(rental)
            self.db.commit()
            self.db.refresh(rental)
            return rental
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(f"Error creating rental: {e}", original_exception=e)

    def end_rental(self, rental: Rental) -> Rental:
        try:
            rental.end_date = datetime.now(timezone.utc)
            rental.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(rental)
            return rental
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(f"Error ending rental {rental.id}: {e}", original_exception=e)
