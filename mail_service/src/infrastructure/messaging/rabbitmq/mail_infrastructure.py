import pika

class MailServiceInfrastructure:

    ORDERS_EXCHANGE = "orders_exchange"
    
    QUEUE_NAME = "mail_orders_queue"

    BINDINGS = [
        "orders.created",
        "orders.updated",
        "orders.cancelled",
    ]

    def __init__(self, channel: pika.channel.Channel) -> None:
        self._channel = channel

    def setup(self) -> None:
        self._channel.exchange_declare(
            exchange=self.ORDERS_EXCHANGE,
            exchange_type="topic",
            durable=True
        )

        self._channel.queue_declare(
            queue=self.QUEUE_NAME,
            durable=True,
            arguments={
                "x-dead-letter-exchange": f"{self.QUEUE_NAME}_dlx",
            }
        )

        self._setup_dlq()

        for routing_key in self.BINDINGS:
            self._channel.queue_bind(
                queue=self.QUEUE_NAME,
                exchange=self.ORDERS_EXCHANGE,
                routing_key=routing_key
            )

    def _setup_dlq(self) -> None:
        dlx_name = f"{self.QUEUE_NAME}_dlx"
        dlq_name = f"{self.QUEUE_NAME}_dlq"

        self._channel.exchange_declare(
            exchange=dlx_name,
            exchange_type="fanout",
            durable=True
        )

        self._channel.queue_declare(
            queue=dlq_name,
            durable=True
        )

        self._channel.queue_bind(
            queue=dlq_name,
            exchange=dlx_name
        )