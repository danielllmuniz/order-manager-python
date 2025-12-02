from order_service.src.application.dtos.order_dto import GetOrderRequest, OrderResponse
from order_service.src.domain.exceptions.order_exceptions import OrderNotFoundException
from order_service.src.domain.interfaces.order_repository import IOrderRepository


class GetOrderUseCase:
    def __init__(self, order_repository: IOrderRepository) -> None:
        self._order_repository = order_repository

    def execute(self, request: GetOrderRequest) -> OrderResponse:
        order = self._order_repository.find_by_id(request.order_id)

        if order is None:
            raise OrderNotFoundException(request.order_id)

        return OrderResponse.from_entity(order)
