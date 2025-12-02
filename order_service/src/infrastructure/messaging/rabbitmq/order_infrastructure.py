import pika

class OrderServiceInfrastructure:
    EXCHANGE_NAME = "orders_exchange"
    EXCHANGE_TYPE = "topic"

    ROUTING_KEYS = {
        "created": "orders.created",
        "updated": "orders.updated",
    }

    def __init__(self, channel: pika.channel.Channel) -> None:
        self._channel = channel

    def setup(self) -> None:
        self._channel.exchange_declare(
            exchange=self.EXCHANGE_NAME,
            exchange_type=self.EXCHANGE_TYPE,
            durable=True
        )
