from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from db.rental_model import Rental

class IRentalService(ABC):
    @abstractmethod
    def get_all_rentals(self) -> List[Rental]:
        pass

    @abstractmethod
    def create_rental(self, car_id: UUID, customer_name: str) -> Rental:
        pass

    @abstractmethod
    def end_rental(self, rental_id: UUID) -> Rental:
        pass
