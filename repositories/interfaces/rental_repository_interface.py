from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from db.rental_model import Rental

class IRentalRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Rental]:
        pass

    @abstractmethod
    async def create(self, car_id: UUID, customer_name: str) -> Rental:
        pass

    @abstractmethod
    async def end_rental(self, rental: Rental) -> Rental:
        pass

    @abstractmethod
    async def get_active_rental_by_car_id(self, car_id: UUID) -> Optional[Rental]:
        pass
