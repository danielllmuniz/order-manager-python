from order_service.src.application.dtos.order_dto import GetOrderRequest, OrderResponse
from order_service.src.domain.exceptions.order_exceptions import OrderNotFoundException
from order_service.src.domain.interfaces.order_repository import IOrderRepository
from order_service.src.domain.interfaces.redis_repository import IRedisRepository
from order_service.src.domain.entities.order import Order


class GetOrderUseCase:
    def __init__(
        self,
        order_repository: IOrderRepository,
        redis_repository: IRedisRepository | None = None,
    ) -> None:
        self._order_repository = order_repository
        self._redis_repository = redis_repository

    def execute(self, request: GetOrderRequest) -> OrderResponse:
        cache_key = f"order:{request.order_id}"

        # Try to get from cache first
        if self._redis_repository:
            cached_data = self._redis_repository.get(cache_key)
            if cached_data:
                order = Order.from_dict(cached_data)
                return OrderResponse.from_entity(order)

        # If not in cache, get from repository
        order = self._order_repository.find_by_id(request.order_id)

        if order is None:
            raise OrderNotFoundException(request.order_id)

        # Cache the order
        if self._redis_repository:
            self._redis_repository.set(cache_key, order.to_dict(), ttl=3600)

        return OrderResponse.from_entity(order)
