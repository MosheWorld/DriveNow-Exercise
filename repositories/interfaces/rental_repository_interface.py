from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.entities.rental import RentalEntity

class IRentalRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[RentalEntity]:
        pass

    @abstractmethod
    async def create(self, car_id: UUID, customer_name: str) -> RentalEntity:
        pass

    @abstractmethod
    async def end_rental(self, rental: RentalEntity) -> RentalEntity:
        pass

    @abstractmethod
    async def get_active_rental_by_car_id(self, car_id: UUID) -> Optional[RentalEntity]:
        pass
