from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


@dataclass
class Order:
    status: OrderStatus
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["status"] = self.status.value
        data["created_at"] = self.created_at
        data["updated_at"] = self.updated_at
        if self.id:
            data["_id"] = self.id
            del data["id"]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        if "_id" in data:
            data["id"] = data.pop("_id")
        data["status"] = OrderStatus(data["status"])
        return cls(**data)
