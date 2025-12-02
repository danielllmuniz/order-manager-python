from order_service.src.application.dtos.order_dto import OrderResponse
from order_service.src.domain.entities.order import Order
from order_service.src.domain.value_objects.order_status import OrderStatus
from order_service.src.domain.interfaces.order_repository import IOrderRepository
from order_service.src.domain.interfaces.order_publisher import IOrderPublisher
from order_service.src.domain.interfaces.redis_repository import IRedisRepository


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: IOrderRepository,
        order_publisher: IOrderPublisher,
        redis_repository: IRedisRepository | None = None,
    ) -> None:
        self._order_repository = order_repository
        self._order_publisher = order_publisher
        self._redis_repository = redis_repository

    def execute(self) -> OrderResponse:
        order = Order(status=OrderStatus.CREATED)

        order_id = self._order_repository.create(order)

        order.id = order_id

        # Cache the order
        if self._redis_repository:
            cache_key = f"order:{order_id}"
            self._redis_repository.set(cache_key, order.to_dict(), ttl=3600)

        self._order_publisher.publish_order_created(str(order_id))

        return OrderResponse.from_entity(order)
