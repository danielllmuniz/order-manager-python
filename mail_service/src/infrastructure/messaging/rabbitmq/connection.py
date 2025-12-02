import pika

from mail_service.src.infrastructure.messaging.rabbitmq.config import RabbitMQConfig


class RabbitMQConnection:
    def __init__(self, config: RabbitMQConfig | None = None) -> None:
        self._config = config or RabbitMQConfig()
        self._connection: pika.BlockingConnection | None = None

    def get_connection(self) -> pika.BlockingConnection:
        if self._connection is None or self._connection.is_closed:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self._config.host,
                    port=self._config.port,
                    credentials=pika.PlainCredentials(
                        username=self._config.username,
                        password=self._config.password
                    ),
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
        return self._connection

    def create_channel(self) -> pika.channel.Channel:
        return self.get_connection().channel()

    def close(self) -> None:
        if self._connection and not self._connection.is_closed:
            self._connection.close()
            self._connection = None
