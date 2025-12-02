from datetime import datetime
from bson.objectid import ObjectId

from order_service.src.infrastructure.database.mongodb.connection import MongoDBConnection
from order_service.src.infrastructure.database.mongodb.order import Order, OrderStatus


class OrderRepository:
    COLLECTION_NAME = "orders"

    def __init__(self, connection: MongoDBConnection) -> None:
        self._connection = connection
        self._db = self._connection.get_database()
        self._collection = self._db[self.COLLECTION_NAME]

    def create(self, order: Order) -> str:
        order_dict = order.to_dict()
        result = self._collection.insert_one(order_dict)
        return str(result.inserted_id)

    def find_by_id(self, order_id: str) -> Order | None:
        try:
            document = self._collection.find_one({"_id": ObjectId(order_id)})
            if document:
                return Order.from_dict(document)
        except Exception:
            pass
        return None

    def update_status(self, order_id: str, status: OrderStatus) -> bool:
        try:
            result = self._collection.update_one(
                {"_id": ObjectId(order_id)},
                {
                    "$set": {
                        "status": status.value,
                        "updated_at": datetime.utcnow(),
                    }
                },
            )
            return result.modified_count > 0
        except Exception:
            return False
