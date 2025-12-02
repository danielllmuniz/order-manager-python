from abc import ABC, abstractmethod

from order_service.src.application.dtos.order_dto import OrderResponse

class CreateOrderUseCase(ABC):
    @abstractmethod
    def execute(self) -> OrderResponse:
        pass
