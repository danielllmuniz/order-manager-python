from dataclasses import dataclass
import os


@dataclass
class RedisConfig:
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    password: str = os.getenv("REDIS_PASSWORD", "redis_password")
    db: int = int(os.getenv("REDIS_DB", "0"))
    decode_responses: bool = True
