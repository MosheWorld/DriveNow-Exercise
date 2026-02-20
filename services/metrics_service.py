from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST
from typing import Tuple
from services.interfaces.metrics_service_interface import IMetricsService

HTTP_REQUEST_DURATION = Histogram('drivenow_http_request_duration_seconds', 'Histogram of HTTP request processing duration in seconds', ['method', 'endpoint'])

class MetricsService(IMetricsService):
    def record_request_time(self, method: str, endpoint: str, execution_time_seconds: float) -> None:
        HTTP_REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(execution_time_seconds)

    def get_metrics_data(self) -> Tuple[bytes, str]:
        return generate_latest(), CONTENT_TYPE_LATEST
