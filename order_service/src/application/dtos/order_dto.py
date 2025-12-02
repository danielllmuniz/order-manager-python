from dataclasses import dataclass
from datetime import datetime

@dataclass
class GetOrderRequest:
    order_id: str

@dataclass
class OrderResponse:
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, order) -> "OrderResponse":
        return cls(
            id=str(order.id),
            status=order.status.value,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
