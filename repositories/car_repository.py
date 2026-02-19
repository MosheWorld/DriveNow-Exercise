from sqlalchemy.orm import Session
from db.models import Car, CarStatus

class CarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Car).all()

    def get_by_id(self, car_id):
        return self.db.query(Car).filter(Car.id == car_id).first()

    def create(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> Car:
        car = Car(model=model, year=year, status=status)
        self.db.add(car)
        self.db.commit()
        self.db.refresh(car)
        return car
