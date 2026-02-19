from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from db.rental_model import Rental

class RentalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Rental]:
        return self.db.query(Rental).all()

    def get_by_id(self, rental_id: UUID) -> Optional[Rental]:
        return self.db.query(Rental).filter(Rental.id == rental_id).first()

    def create(self, car_id: UUID, customer_name: str) -> Rental:
        rental = Rental(car_id=car_id, customer_name=customer_name)
        self.db.add(rental)
        self.db.commit()
        self.db.refresh(rental)
        return rental

    def end_rental(self, rental: Rental) -> Rental:
        rental.end_date = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(rental)
        return rental
