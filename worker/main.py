import json
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import time
from prometheus_client import start_http_server, Gauge
from common.config import settings
from common.message_schema import MessageEvent
import common.constants as constants
from common.logger import Logger

logger = Logger()

AVAILABLE_CARS_GAUGE = Gauge('drivenow_available_cars_total', 'Total number of cars currently available for rent in the fleet')
ACTIVE_RENTALS_GAUGE = Gauge('drivenow_active_rentals_total', 'Total number of active rentals that have not yet been ended')

def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
    try:
        data = json.loads(body)
        event = MessageEvent(**data)
        event_type = event.event_type
        
        if event_type in (constants.EVENT_CAR_CREATED_AVAILABLE, constants.EVENT_CAR_STATUS_CHANGED_TO_AVAILABLE):
            AVAILABLE_CARS_GAUGE.inc()
        elif event_type == constants.EVENT_CAR_STATUS_CHANGED_FROM_AVAILABLE:
            AVAILABLE_CARS_GAUGE.dec()
        elif event_type == constants.EVENT_RENTAL_CREATED:
            ACTIVE_RENTALS_GAUGE.inc()
            AVAILABLE_CARS_GAUGE.dec()
        elif event_type == constants.EVENT_RENTAL_ENDED:
            ACTIVE_RENTALS_GAUGE.dec()
            AVAILABLE_CARS_GAUGE.inc()
            
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def start_worker() -> None:
    start_http_server(8001)
    
    connection = None
    while not connection:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        except Exception:
            logger.warning("RabbitMQ not ready yet, retrying in 2 seconds...")
            time.sleep(2)
            
    channel = connection.channel()
    channel.queue_declare(queue=constants.METRICS_QUEUE_NAME, durable=True)

    channel.basic_consume(queue=constants.METRICS_QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    start_worker()
