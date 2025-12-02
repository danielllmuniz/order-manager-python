from dataclasses import dataclass
import os


@dataclass
class RabbitMQConfig:
    host: str = os.getenv("RABBITMQ_HOST", "localhost")
    port: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    username: str = os.getenv("RABBITMQ_USERNAME", "admin")
    password: str = os.getenv("RABBITMQ_PASSWORD", "admin")
