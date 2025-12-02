from abc import ABC, abstractmethod
from typing import Any, Optional


class IRedisRepository(ABC):
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def expire(self, key: str, ttl: int) -> bool:
        pass

    @abstractmethod
    def ttl(self, key: str) -> Optional[int]:
        pass

    @abstractmethod
    def flush_all(self) -> bool:
        pass

    @abstractmethod
    def get_many(self, keys: list[str]) -> dict[str, Any]:
        pass

    @abstractmethod
    def set_many(self, data: dict[str, Any], ttl: Optional[int] = None) -> bool:
        pass
