import json
from typing import Any, Optional

from order_service.src.application.ports.logger import ILogger
from order_service.src.domain.interfaces.redis_repository import IRedisRepository
from order_service.src.infrastructure.cache.redis.connection import RedisConnection


class RedisRepository(IRedisRepository):
    def __init__(self, connection: RedisConnection, logger: ILogger | None = None) -> None:
        self._connection = connection
        self._client = self._connection.get_connection()
        self._logger = logger

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        try:
            if isinstance(value, str):
                data = value
            else:
                data = json.dumps(value)

            self._client.set(key, data, ex=ttl)
            if self._logger:
                self._logger.debug(f"Value cached in Redis: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error caching value in Redis {key}: {str(e)}")
            return False

    def get(self, key: str) -> Optional[Any]:
        try:
            value = self._client.get(key)
            if value is None:
                if self._logger:
                    self._logger.debug(f"Cache miss for key: {key}")
                return None

            try:
                result = json.loads(value)
                if self._logger:
                    self._logger.debug(f"Cache hit for key: {key}")
                return result
            except json.JSONDecodeError:
                if self._logger:
                    self._logger.debug(f"Cache hit for key: {key}")
                return value
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error retrieving value from Redis {key}: {str(e)}")
            return None

    def delete(self, key: str) -> bool:
        try:
            result = self._client.delete(key) > 0
            if result and self._logger:
                self._logger.debug(f"Cache key deleted: {key}")
            elif not result and self._logger:
                self._logger.debug(f"Cache key not found: {key}")
            return result
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error deleting cache key {key}: {str(e)}")
            return False

    def exists(self, key: str) -> bool:
        try:
            return self._client.exists(key) > 0
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error checking cache key existence {key}: {str(e)}")
            return False

    def expire(self, key: str, ttl: int) -> bool:
        try:
            result = self._client.expire(key, ttl)
            if result and self._logger:
                self._logger.debug(f"Cache key TTL updated: {key} (TTL: {ttl}s)")
            return result
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error updating cache key TTL {key}: {str(e)}")
            return False
