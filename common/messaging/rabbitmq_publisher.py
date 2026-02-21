import aio_pika
from common.interfaces.message_publisher_interface import IMessagePublisher
from common.interfaces.logger_interface import ILogger
from common.messaging.messaging_constants import METRICS_QUEUE_NAME
from common.messaging.message_schema import MessageEvent
from common.config import settings

class RabbitMQPublisher(IMessagePublisher):
    def __init__(self, logger: ILogger) -> None:
        self.logger = logger
        self.host: str = settings.RABBITMQ_HOST
        self.connection = None
        self.channel = None

    async def _connect(self) -> None:
        if not self.connection or self.connection.is_closed:
            try:
                self.connection = await aio_pika.connect_robust(host=self.host)
                self.channel = await self.connection.channel()
                await self.channel.declare_queue(METRICS_QUEUE_NAME, durable=True)
            except Exception as e:
                self.logger.error(f"Failed to connect to RabbitMQ: {e}")

    async def publish_event(self, event_type: str, payload: dict) -> None:
        await self._connect()
        if not self.channel:
            self.logger.error(f"Cannot publish event {event_type}, no RMQ channel")
            return
        
        message_event = MessageEvent(event_type=event_type, payload=payload)
        try:
            message = aio_pika.Message(body=message_event.to_json().encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT)
            await self.channel.default_exchange.publish(message, routing_key=METRICS_QUEUE_NAME)
            self.logger.info(f"Published message queue event: {event_type}")
        except Exception as e:
            self.logger.error(f"Failed to publish event: {e}")
            self.connection = None
