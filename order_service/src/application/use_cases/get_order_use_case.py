from order_service.src.application.dtos.order_dto import GetOrderRequest, OrderResponse
from order_service.src.application.ports.logger import ILogger
from order_service.src.domain.exceptions.order_exceptions import OrderNotFoundException
from order_service.src.domain.interfaces.order_repository import IOrderRepository
from order_service.src.domain.interfaces.redis_repository import IRedisRepository
from order_service.src.domain.entities.order import Order


class GetOrderUseCase:
    def __init__(
        self,
        order_repository: IOrderRepository,
        logger: ILogger,
        redis_repository: IRedisRepository | None = None,
    ) -> None:
        self._order_repository = order_repository
        self._logger = logger
        self._redis_repository = redis_repository

    def execute(self, request: GetOrderRequest) -> OrderResponse:
        self._logger.info(f"Fetching order with ID: {request.order_id}")
        cache_key = f"order:{request.order_id}"

        # Try to get from cache first
        if self._redis_repository:
            cached_data = self._redis_repository.get(cache_key)
            if cached_data:
                order = Order.from_dict(cached_data)
                self._logger.debug(f"Order found in cache: {request.order_id}")
                return OrderResponse.from_entity(order)

        self._logger.debug(f"Fetching order from repository: {request.order_id}")
        order = self._order_repository.find_by_id(request.order_id)

        if order is None:
            self._logger.warning(f"Order not found: {request.order_id}")
            raise OrderNotFoundException(request.order_id)

        if self._redis_repository:
            self._redis_repository.set(cache_key, order.to_dict(), ttl=3600)
            self._logger.debug(f"Order cached with key: {cache_key}")

        self._logger.info(f"Order fetched successfully: {request.order_id}")
        return OrderResponse.from_entity(order)
