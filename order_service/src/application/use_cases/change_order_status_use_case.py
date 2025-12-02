from order_service.src.application.dtos.order_dto import OrderResponse
from order_service.src.domain.exceptions.order_exceptions import OrderNotFoundException
from order_service.src.domain.value_objects.order_status import OrderStatus
from order_service.src.domain.interfaces.order_repository import IOrderRepository
from order_service.src.domain.interfaces.order_publisher import IOrderPublisher


class ChangeOrderStatusUseCase:
    def __init__(
        self,
        order_repository: IOrderRepository,
        order_publisher: IOrderPublisher,
    ) -> None:
        self._order_repository = order_repository
        self._order_publisher = order_publisher

    def execute(self, order_id: str) -> OrderResponse:
        order = self._order_repository.find_by_id(order_id)

        if order is None:
            raise OrderNotFoundException(order_id)

        next_status = self._get_next_status(order.status)

        self._order_repository.update_status(order_id, next_status)

        self._order_publisher.publish_order_updated(order_id, next_status.value)

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
