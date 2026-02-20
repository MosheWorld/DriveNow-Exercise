import httpx
from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from common.logger import Logger
from common.config import settings

router = APIRouter(prefix="/metrics", tags=["metrics"])
logger = Logger()

@router.get("")
async def get_metrics() -> Response:
    api_metrics = generate_latest().decode("utf-8")
    
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
    return Response(content=combined, media_type=CONTENT_TYPE_LATEST)
