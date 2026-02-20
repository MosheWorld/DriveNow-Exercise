import json
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import time
from prometheus_client import start_http_server, Gauge
from common.config import settings
from common.messaging.message_schema import MessageEvent
import common.messaging.messaging_constants as constants
from common.logger import Logger

logger = Logger()

AVAILABLE_CARS_GAUGE = Gauge('drivenow_available_cars_total', 'Total number of cars currently available for rent in the fleet')
ACTIVE_RENTALS_GAUGE = Gauge('drivenow_active_rentals_total', 'Total number of active rentals that have not yet been ended')

def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
    try:
        data = json.loads(body)
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

def start_worker() -> None:
    logger.info("Starting Metrics Worker service...")
    start_http_server(8001)
    logger.info("Metrics HTTP server started on port 8001")
    
    connection = None
    while not connection:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        except Exception:
            logger.warning("RabbitMQ not ready yet, retrying in 2 seconds...")
            time.sleep(2)
            
    channel = connection.channel()
    channel.queue_declare(queue=constants.METRICS_QUEUE_NAME, durable=True)

    logger.info(f"Connected to RabbitMQ. Waiting for messages on queue: {constants.METRICS_QUEUE_NAME}")
    channel.basic_consume(queue=constants.METRICS_QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()
