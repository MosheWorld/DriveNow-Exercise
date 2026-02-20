import json
import pika
from common.interfaces.message_publisher_interface import IMessagePublisher
from common.interfaces.logger_interface import ILogger
from common.constants import METRICS_QUEUE_NAME
from common.message_schema import MessageEvent
from common.config import settings

class RabbitMQPublisher(IMessagePublisher):
    def __init__(self, logger: ILogger) -> None:
        self.logger = logger
        self.host = settings.RABBITMQ_HOST
        self.connection = None
        self.channel = None

    def _connect(self) -> None:
        if not self.connection or self.connection.is_closed:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=METRICS_QUEUE_NAME, durable=True)
            except Exception as e:
                self.logger.error(f"Failed to connect to RabbitMQ: {e}")

    def publish_event(self, event_type: str, payload: dict) -> None:
        self._connect()
        if not self.channel:
            self.logger.error(f"Cannot publish event {event_type}, no RMQ channel")
            return
        
        message_event = MessageEvent(event_type=event_type, payload=payload)
        try:
            self.channel.basic_publish(exchange='', routing_key=METRICS_QUEUE_NAME, body=message_event.to_json(), properties=pika.BasicProperties(delivery_mode=2))
            self.logger.info(f"Published message queue event: {event_type}")
        except Exception as e:
            self.logger.error(f"Failed to publish event: {e}")
            self.connection = None
