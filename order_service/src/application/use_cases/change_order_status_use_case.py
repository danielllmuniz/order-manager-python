from order_service.src.application.dtos.order_dto import OrderResponse
from order_service.src.application.ports.logger import ILogger
from order_service.src.domain.exceptions.order_exceptions import OrderNotFoundException
from order_service.src.domain.value_objects.order_status import OrderStatus
from order_service.src.domain.interfaces.order_repository import IOrderRepository
from order_service.src.domain.interfaces.order_publisher import IOrderPublisher
from order_service.src.domain.interfaces.redis_repository import IRedisRepository


class ChangeOrderStatusUseCase:
    def __init__(
        self,
        order_repository: IOrderRepository,
        order_publisher: IOrderPublisher,
        logger: ILogger,
        redis_repository: IRedisRepository | None = None,
    ) -> None:
        self._order_repository = order_repository
        self._order_publisher = order_publisher
        self._logger = logger
        self._redis_repository = redis_repository

    def execute(self, order_id: str) -> OrderResponse:
        self._logger.info(f"Changing status for order: {order_id}")
        order = self._order_repository.find_by_id(order_id)

        if order is None:
            self._logger.warning(f"Order not found for status change: {order_id}")
            raise OrderNotFoundException(order_id)

        current_status = order.status.value
        next_status = self._get_next_status(order.status)
        self._logger.info(f"Order {order_id} status change: {current_status} -> {next_status.value}")

        self._order_repository.update_status(order_id, next_status)

        # Invalidate cache
        if self._redis_repository:
            cache_key = f"order:{order_id}"
            self._redis_repository.delete(cache_key)
            self._logger.debug(f"Cache invalidated for order: {order_id}")

        self._order_publisher.publish_order_updated(order_id, next_status.value)
        self._logger.info(f"Order status update event published: {order_id}")

        order.status = next_status

        return OrderResponse.from_entity(order)

    @staticmethod
    def _get_next_status(current_status: OrderStatus) -> OrderStatus:
        status_sequence = {
            OrderStatus.CREATED: OrderStatus.PROCESSING,
            OrderStatus.PROCESSING: OrderStatus.SHIPPED,
            OrderStatus.SHIPPED: OrderStatus.DELIVERED,
            OrderStatus.DELIVERED: OrderStatus.DELIVERED,  # Already at final state
        }
        return status_sequence.get(current_status, current_status)
