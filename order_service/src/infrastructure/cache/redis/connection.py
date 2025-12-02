import redis
from redis.client import Redis

from order_service.src.infrastructure.cache.redis.config import RedisConfig


class RedisConnection:
    def __init__(self, config: RedisConfig | None = None) -> None:
        self._config = config or RedisConfig()
        self._client: Redis | None = None

    def get_connection(self) -> Redis:
        if self._client is None:
            self._client = redis.Redis(
                host=self._config.host,
                port=self._config.port,
                password=self._config.password,
                db=self._config.db,
                decode_responses=self._config.decode_responses,
            )
        return self._client

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
