from abc import ABC, abstractmethod
from typing import Tuple

class IMetricsService(ABC):
    @abstractmethod
    def increment_active_cars(self, amount: int = 1) -> None:
        pass

    @abstractmethod
    def decrement_active_cars(self, amount: int = 1) -> None:
        pass

    @abstractmethod
    def increment_ongoing_rentals(self, amount: int = 1) -> None:
        pass

    @abstractmethod
    def decrement_ongoing_rentals(self, amount: int = 1) -> None:
        pass

    @abstractmethod
    def record_request_time(self, method: str, endpoint: str, execution_time_seconds: float) -> None:
        pass

    @abstractmethod
    def get_metrics_data(self) -> Tuple[bytes, str]:
        pass
