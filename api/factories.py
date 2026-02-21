from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from repositories.car_repository import CarRepository
from repositories.rental_repository import RentalRepository
from services.car_service import CarService
from services.rental_service import RentalService
from services.interfaces.car_service_interface import ICarService
from services.interfaces.rental_service_interface import IRentalService
from services.interfaces.metrics_service_interface import IMetricsService
from services.metrics_service import MetricsService
from common.messaging.rabbitmq_publisher import RabbitMQPublisher
from common.logger import Logger

def car_service_factory(db: AsyncSession = Depends(get_db)) -> ICarService:
    logger = Logger()
    event_publisher = RabbitMQPublisher(logger)
    repository = CarRepository(db)
    return CarService(logger, event_publisher, repository)

def rental_service_factory(db: AsyncSession = Depends(get_db)) -> IRentalService:
    logger = Logger()
    event_publisher = RabbitMQPublisher(logger)
    rental_repo = RentalRepository(db)
    car_repo = CarRepository(db)
    return RentalService(logger, event_publisher, rental_repo, car_repo)

def metrics_service_factory() -> IMetricsService:
    return MetricsService()
