import json
import pika

from order_service.src.application.ports.logger import ILogger
from order_service.src.domain.interfaces.order_publisher import IOrderPublisher
from order_service.src.infrastructure.messaging.rabbitmq.order_infrastructure import OrderServiceInfrastructure

class OrderPublisher(IOrderPublisher):
    def __init__(self, channel: pika.channel.Channel, logger: ILogger | None = None) -> None:
        self._channel = channel
        self._logger = logger
        self._exchange = OrderServiceInfrastructure.EXCHANGE_NAME
        self._routing_keys = OrderServiceInfrastructure.ROUTING_KEYS

    def _publish(self, routing_key: str, body: dict) -> None:
        try:
            self._channel.basic_publish(
                exchange=self._exchange,
                routing_key=routing_key,
                body=json.dumps(body),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json"
                )
            )
            if self._logger:
                self._logger.debug(f"Message published to {routing_key}: {body}")
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error publishing message to {routing_key}: {str(e)}")
            raise

    def publish_order_created(self, order_id: str) -> None:
        if self._logger:
            self._logger.info(f"Publishing order created event for order: {order_id}")
        self._publish(
            routing_key=self._routing_keys["created"],
            body={
                "event": "order_created",
                "order_id": order_id,
            }
        )

    def publish_order_updated(self, order_id: str, status: str) -> None:
        if self._logger:
            self._logger.info(f"Publishing order updated event for order: {order_id} with status: {status}")
        self._publish(
            routing_key=self._routing_keys["updated"],
            body={
                "event": "order_updated",
                "order_id": order_id,
                "status": status
            }
        )
