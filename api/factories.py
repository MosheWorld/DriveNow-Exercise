from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from repositories.car_repository import CarRepository
from repositories.rental_repository import RentalRepository
from services.car_service import CarService
from services.rental_service import RentalService
from services.interfaces.car_service_interface import ICarService
from services.interfaces.rental_service_interface import IRentalService
from services.metrics_service import MetricsService
from common.logger import Logger

def car_service_factory(db: Session = Depends(get_db)) -> ICarService:
    logger = Logger()
    metrics = MetricsService()
    repository = CarRepository(db)
    return CarService(logger, metrics, repository)

def rental_service_factory(db: Session = Depends(get_db)) -> IRentalService:
    logger = Logger()
    metrics = MetricsService()
    rental_repo = RentalRepository(db)
    car_repo = CarRepository(db)
    return RentalService(logger, metrics, rental_repo, car_repo)
