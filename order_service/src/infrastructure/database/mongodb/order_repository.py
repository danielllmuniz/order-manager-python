from datetime import datetime
from bson.objectid import ObjectId

from order_service.src.domain.interfaces.order_repository import IOrderRepository
from order_service.src.domain.entities.order import Order
from order_service.src.domain.value_objects.order_status import OrderStatus
from order_service.src.infrastructure.database.mongodb.connection import MongoDBConnection


class OrderRepository(IOrderRepository):
    COLLECTION_NAME = "orders"

    def __init__(self, connection: MongoDBConnection) -> None:
        self._connection = connection
        self._db = self._connection.get_database()
        self._collection = self._db[self.COLLECTION_NAME]

    def create(self, order: Order) -> ObjectId:
        order_dict = order.to_dict()
        result = self._collection.insert_one(order_dict)
        return result.inserted_id

    def find_by_id(self, order_id: ObjectId | str) -> Order | None:
        try:
            obj_id = order_id if isinstance(order_id, ObjectId) else ObjectId(order_id)
            document = self._collection.find_one({"_id": obj_id})
            if document:
                return Order.from_dict(document)
        except Exception:
            pass
        return None

    def update_status(self, order_id: ObjectId | str, status: OrderStatus) -> bool:
        try:
            obj_id = order_id if isinstance(order_id, ObjectId) else ObjectId(order_id)
            result = self._collection.update_one(
                {"_id": obj_id},
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

