from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from db.car_model import Car, CarStatus

class ICarRepository(ABC):
    @abstractmethod
    def get_all(self, status: Optional[CarStatus] = None) -> List[Car]:
        pass

    @abstractmethod
    def get_by_id(self, car_id: UUID) -> Optional[Car]:
        pass

    @abstractmethod
    def create(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> Car:
        pass

    @abstractmethod
    def update(self, car: Car) -> Car:
        pass
