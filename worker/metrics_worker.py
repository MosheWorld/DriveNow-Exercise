import json
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
import asyncio
from prometheus_client import start_http_server, Gauge
from common.config import settings
from common.messaging.message_schema import MessageEvent
import common.messaging.messaging_constants as constants
from common.logger import Logger

logger = Logger()

AVAILABLE_CARS_GAUGE = Gauge('drivenow_available_cars_total', 'Total number of cars currently available for rent in the fleet')
ACTIVE_RENTALS_GAUGE = Gauge('drivenow_active_rentals_total', 'Total number of active rentals that have not yet been ended')

async def process_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        try:
            data = json.loads(message.body)
            event = MessageEvent(**data)
            event_type = event.event_type
            
            logger.info(f"Worker received event: {event_type}")
            
            if event_type in (constants.EVENT_CAR_CREATED_AVAILABLE, constants.EVENT_CAR_STATUS_CHANGED_TO_AVAILABLE):
                logger.info("Incrementing available cars gauge")
                AVAILABLE_CARS_GAUGE.inc()
            elif event_type == constants.EVENT_CAR_STATUS_CHANGED_FROM_AVAILABLE:
                logger.info("Decrementing available cars gauge")
                AVAILABLE_CARS_GAUGE.dec()
            elif event_type == constants.EVENT_RENTAL_CREATED:
                logger.info("Incrementing active rentals and decrementing available cars gauges")
                ACTIVE_RENTALS_GAUGE.inc()
                AVAILABLE_CARS_GAUGE.dec()
            elif event_type == constants.EVENT_RENTAL_ENDED:
                logger.info("Decrementing active rentals and incrementing available cars gauges")
                ACTIVE_RENTALS_GAUGE.dec()
                AVAILABLE_CARS_GAUGE.inc()
            else:
                logger.warning(f"Worker received unknown event type: {event_type}")
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")

async def start_worker() -> None:
    logger.info("Starting Metrics Worker service...")
    start_http_server(8001)
    logger.info("Metrics HTTP server started on port 8001")
    
    connection = None
    while not connection:
        try:
            connection = await aio_pika.connect_robust(host=settings.RABBITMQ_HOST)
        except Exception:
            logger.warning("RabbitMQ not ready yet, retrying in 2 seconds...")
            await asyncio.sleep(2)
            
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(constants.METRICS_QUEUE_NAME, durable=True)

        logger.info(f"Connected to RabbitMQ. Waiting for messages on queue: {constants.METRICS_QUEUE_NAME}")
        await queue.consume(process_message)
        
        # Wait until termination
        await asyncio.Future()

if __name__ == '__main__':
    try:
        asyncio.run(start_worker())
    except KeyboardInterrupt:
        pass
