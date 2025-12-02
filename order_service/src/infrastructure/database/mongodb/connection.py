from pymongo import MongoClient
from pymongo.database import Database

from order_service.src.infrastructure.database.mongodb.config import MongoDBConfig
class MongoDBConnection:
    def __init__(self, config: MongoDBConfig | None = None) -> None:
        self._config = config or MongoDBConfig()
        self._client: MongoClient | None = None

    def get_connection(self) -> MongoClient:
        if self._client is None:
            self._client = MongoClient(
                host=self._config.host,
                port=self._config.port,
                username=self._config.username,
                password=self._config.password,
            )
        return self._client

    def get_database(self, db_name: str | None = None) -> Database:
        return self.get_connection()[db_name or self._config.database]

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
