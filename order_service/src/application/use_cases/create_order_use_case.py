from order_service.src.application.dtos.order_dto import OrderResponse
from order_service.src.domain.entities.order import Order
from order_service.src.domain.value_objects.order_status import OrderStatus
from order_service.src.domain.interfaces.order_repository import IOrderRepository
from order_service.src.domain.interfaces.order_publisher import IOrderPublisher


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: IOrderRepository,
        order_publisher: IOrderPublisher,
    ) -> None:
        self._order_repository = order_repository
        self._order_publisher = order_publisher

    def execute(self) -> OrderResponse:
        order = Order(status=OrderStatus.CREATED)

        order_id = self._order_repository.create(order)

        self._order_publisher.publish_order_created(str(order_id))

        order.id = order_id

        return OrderResponse.from_entity(order)
