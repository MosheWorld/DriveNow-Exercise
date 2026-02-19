from sqlalchemy.orm import Session
from db.models import Rental

class RentalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Rental).all()

    def create(self, car_id, customer_name: str) -> Rental:
        rental = Rental(car_id=car_id, customer_name=customer_name)
        self.db.add(rental)
        self.db.commit()
        self.db.refresh(rental)
        return rental
