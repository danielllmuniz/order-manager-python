from abc import ABC, abstractmethod


class IOrderPublisher(ABC):
    @abstractmethod
    def publish_order_created(self, order_id: str) -> None:
        pass

    @abstractmethod
    def publish_order_updated(self, order_id: str, status: str) -> None:
        pass
