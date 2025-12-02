import json
from typing import Any, Optional

from order_service.src.domain.interfaces.redis_repository import IRedisRepository
from order_service.src.infrastructure.cache.redis.connection import RedisConnection


class RedisRepository(IRedisRepository):
    def __init__(self, connection: RedisConnection) -> None:
        self._connection = connection
        self._client = self._connection.get_connection()

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        try:
            if isinstance(value, str):
                data = value
            else:
                data = json.dumps(value)

            self._client.set(key, data, ex=ttl)
            return True
        except Exception:
            return False

    def get(self, key: str) -> Optional[Any]:
        try:
            value = self._client.get(key)
            if value is None:
                return None

            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except Exception:
            return None

    def delete(self, key: str) -> bool:
        try:
            return self._client.delete(key) > 0
        except Exception:
            return False

    def exists(self, key: str) -> bool:
        try:
            return self._client.exists(key) > 0
        except Exception:
            return False

    def expire(self, key: str, ttl: int) -> bool:
        try:
            return self._client.expire(key, ttl)
        except Exception:
            return False
