from fastapi import APIRouter, Response
from services.metrics_service import MetricsService

router = APIRouter(prefix="/metrics", tags=["metrics"])
metrics_service = MetricsService()

@router.get("")
def get_metrics() -> Response:
    data, content_type = metrics_service.get_metrics_data()
    return Response(content=data, media_type=content_type)
