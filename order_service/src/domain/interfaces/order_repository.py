from abc import ABC, abstractmethod

from order_service.src.infrastructure.database.mongodb.order import Order, OrderStatus


class IOrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order) -> str:
        pass

    @abstractmethod
    def find_by_id(self, order_id: str) -> Order | None:
        pass

    @abstractmethod
    def update_status(self, order_id: str, status: OrderStatus) -> bool:
        pass
