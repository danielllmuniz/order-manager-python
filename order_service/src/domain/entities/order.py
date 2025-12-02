from dataclasses import dataclass, field
from datetime import datetime
from bson.objectid import ObjectId

from order_service.src.domain.value_objects.order_status import OrderStatus


@dataclass
class Order:
    status: OrderStatus
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    id: ObjectId | None = None

    def __post_init__(self):
        if self.id is None:
            self.id = ObjectId()

    def to_dict(self) -> dict:
        return {
            "_id": self.id,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        return cls(
            id=data.get("_id"),
            status=OrderStatus(data["status"]),
            created_at=data.get("created_at", datetime.utcnow()),
            updated_at=data.get("updated_at", datetime.utcnow()),
        )
