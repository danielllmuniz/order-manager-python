import json
import pika

from order_service.src.infrastructure.messaging.rabbitmq.order_infrastructure import OrderServiceInfrastructure

class OrderPublisher:
    def __init__(self, channel: pika.channel.Channel) -> None:
        self._channel = channel
        self._exchange = OrderServiceInfrastructure.EXCHANGE_NAME
        self._routing_keys = OrderServiceInfrastructure.ROUTING_KEYS

    def _publish(self, routing_key: str, body: dict) -> None:
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type="application/json"
            )
        )

    def publish_order_created(self, order_id: str) -> None:
        self._publish(
            routing_key=self._routing_keys["created"],
            body={
                "event": "order_created",
                "order_id": order_id,
            }
        )

    def publish_order_updated(self, order_id: str, status: str) -> None:
        self._publish(
            routing_key=self._routing_keys["updated"],
            body={
                "event": "order_updated",
                "order_id": order_id,
                "status": status
            }
        )
