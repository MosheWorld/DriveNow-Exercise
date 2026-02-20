from prometheus_client import Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from typing import Tuple
from services.interfaces.metrics_service_interface import IMetricsService

AVAILABLE_CARS_GAUGE = Gauge('drivenow_available_cars_total', 'Total number of cars currently available for rent in the fleet')
ACTIVE_RENTALS_GAUGE = Gauge('drivenow_active_rentals_total', 'Total number of active rentals that have not yet been ended')
HTTP_REQUEST_DURATION = Histogram('drivenow_http_request_duration_seconds', 'Histogram of HTTP request processing duration in seconds', ['method', 'endpoint'])

class MetricsService(IMetricsService):
    def increment_active_cars(self, amount: int = 1) -> None:
        AVAILABLE_CARS_GAUGE.inc(amount)

    def decrement_active_cars(self, amount: int = 1) -> None:
        AVAILABLE_CARS_GAUGE.dec(amount)

    def increment_ongoing_rentals(self, amount: int = 1) -> None:
        ACTIVE_RENTALS_GAUGE.inc(amount)

    def decrement_ongoing_rentals(self, amount: int = 1) -> None:
        ACTIVE_RENTALS_GAUGE.dec(amount)

    def record_request_time(self, method: str, endpoint: str, execution_time_seconds: float) -> None:
        HTTP_REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(execution_time_seconds)

    def get_metrics_data(self) -> Tuple[bytes, str]:
        return generate_latest(), CONTENT_TYPE_LATEST
