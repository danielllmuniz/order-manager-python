from datetime import datetime
from bson.objectid import ObjectId

from order_service.src.application.ports.logger import ILogger
from order_service.src.domain.interfaces.order_repository import IOrderRepository
from order_service.src.domain.entities.order import Order
from order_service.src.domain.value_objects.order_status import OrderStatus
from order_service.src.infrastructure.database.mongodb.connection import MongoDBConnection


class OrderRepository(IOrderRepository):
    COLLECTION_NAME = "orders"

    def __init__(self, connection: MongoDBConnection, logger: ILogger | None = None) -> None:
        self._connection = connection
        self._db = self._connection.get_database()
        self._collection = self._db[self.COLLECTION_NAME]
        self._logger = logger

    def create(self, order: Order) -> ObjectId:
        order_dict = order.to_dict()
        result = self._collection.insert_one(order_dict)
        if self._logger:
            self._logger.debug(f"Order inserted in database with ID: {result.inserted_id}")
        return result.inserted_id

    def find_by_id(self, order_id: ObjectId | str) -> Order | None:
        try:
            obj_id = order_id if isinstance(order_id, ObjectId) else ObjectId(order_id)
            document = self._collection.find_one({"_id": obj_id})
            if document:
                if self._logger:
                    self._logger.debug(f"Order found in database: {obj_id}")
                return Order.from_dict(document)
            if self._logger:
                self._logger.debug(f"Order not found in database: {obj_id}")
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error finding order {order_id}: {str(e)}")
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
            if result.modified_count > 0:
                if self._logger:
                    self._logger.debug(f"Order status updated in database: {obj_id} -> {status.value}")
                return True
            if self._logger:
                self._logger.warning(f"No document updated for order: {obj_id}")
            return False
        except Exception as e:
            if self._logger:
                self._logger.error(f"Error updating order status {order_id}: {str(e)}")
            return False

