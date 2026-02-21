import httpx
from fastapi import APIRouter, Response, Depends
from services.interfaces.metrics_service_interface import IMetricsService
from api.factories import metrics_service_factory
from common.logger import Logger
from common.config import settings

router = APIRouter(prefix="/metrics", tags=["metrics"])
logger = Logger()

@router.get("")
async def get_metrics(metrics_service: IMetricsService = Depends(metrics_service_factory)) -> Response:
    """
    Retrieve aggregated, real-time system metrics.

    Merges internal API HTTP metrics with real-time business metrics fetched 
    from the background RabbitMQ worker service.
    """
    api_metrics_raw, content_type = metrics_service.get_metrics_data()
    api_metrics = api_metrics_raw.decode("utf-8")
    
    worker_metrics = ""
    try:
        if settings.WORKER_METRICS_URL:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(f"{settings.WORKER_METRICS_URL}/metrics")
                if res.status_code == 200:
                    worker_metrics = res.text
    except Exception as e:
        logger.error(f"Failed to fetch worker metrics: {e}")
        
    combined = api_metrics + "\n" + worker_metrics
    return Response(content=combined, media_type=content_type)
