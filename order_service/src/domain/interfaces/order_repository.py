from abc import ABC, abstractmethod
from bson.objectid import ObjectId

from order_service.src.domain.entities.order import Order
from order_service.src.domain.value_objects.order_status import OrderStatus


class IOrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order) -> ObjectId:
        pass

    @abstractmethod
    def find_by_id(self, order_id: ObjectId | str) -> Order | None:
        pass

    @abstractmethod
    def update_status(self, order_id: ObjectId | str, status: OrderStatus) -> bool:
        pass
