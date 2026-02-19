from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from db.car_model import Car, CarStatus

class ICarService(ABC):
    @abstractmethod
    def get_all_cars(self, status: Optional[CarStatus] = None) -> List[Car]:
        pass

    @abstractmethod
    def get_car_by_id(self, car_id: UUID) -> Optional[Car]:
        pass

    @abstractmethod
    def create_car(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> Car:
        pass

    @abstractmethod
    def update_car(self, car_id: UUID, model: Optional[str] = None, year: Optional[int] = None, status: Optional[CarStatus] = None) -> Optional[Car]:
        pass
