from dataclasses import dataclass
import os


@dataclass
class MongoDBConfig:
    host: str = os.getenv("MONGODB_HOST", "localhost")
    port: int = int(os.getenv("MONGODB_PORT", "27017"))
    username: str = os.getenv("MONGODB_USERNAME", "admin")
    password: str = os.getenv("MONGODB_PASSWORD", "admin")
    database: str = os.getenv("MONGODB_DATABASE", "order-service")
