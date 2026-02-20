from abc import ABC, abstractmethod
from typing import Tuple

class IMetricsService(ABC):
    @abstractmethod
    def record_request_time(self, method: str, endpoint: str, execution_time_seconds: float) -> None:
        pass

    @abstractmethod
    def get_metrics_data(self) -> Tuple[bytes, str]:
        pass
