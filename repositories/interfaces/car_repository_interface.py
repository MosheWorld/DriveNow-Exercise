from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.entities.car import CarEntity, CarStatus

class ICarRepository(ABC):
    @abstractmethod
    async def get_all(self, status: Optional[CarStatus] = None) -> List[CarEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, car_id: UUID) -> Optional[CarEntity]:
        pass

    @abstractmethod
    async def create(self, model: str, year: int, status: CarStatus = CarStatus.AVAILABLE) -> CarEntity:
        pass

    @abstractmethod
    async def update(self, car: CarEntity) -> CarEntity:
        pass
