from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from domain.entities.rental import RentalEntity

class IRentalService(ABC):
    @abstractmethod
    async def get_all_rentals(self) -> List[RentalEntity]:
        pass

    @abstractmethod
    async def create_rental(self, car_id: UUID, customer_name: str) -> RentalEntity:
        pass

    @abstractmethod
    async def end_rental_by_car_id(self, car_id: UUID) -> RentalEntity:
        pass
