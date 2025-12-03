import pytest
from datetime import datetime
from bson import ObjectId

from order_service.src.domain.entities.order import Order
from order_service.src.domain.value_objects.order_status import OrderStatus


class TestOrderEntity:

    def test_create_order_with_default_status(self):
        order = Order(status=OrderStatus.CREATED)

        assert order.status == OrderStatus.CREATED
        assert order.id is not None
        assert isinstance(order.id, ObjectId)
        assert isinstance(order.created_at, datetime)
        assert isinstance(order.updated_at, datetime)

    def test_create_order_with_custom_id(self):
        custom_id = ObjectId()
        order = Order(status=OrderStatus.CREATED, id=custom_id)

        assert order.id == custom_id

    def test_order_to_dict(self):
        custom_id = ObjectId()
        order = Order(status=OrderStatus.CREATED, id=custom_id)
        order_dict = order.to_dict()

        assert order_dict["_id"] == custom_id
        assert order_dict["status"] == "created"
        assert "created_at" in order_dict
        assert "updated_at" in order_dict

    def test_order_from_dict(self):
        custom_id = ObjectId()
        now = datetime.utcnow()
        data = {
            "_id": custom_id,
            "status": "processing",
            "created_at": now,
            "updated_at": now,
        }

        order = Order.from_dict(data)

        assert order.id == custom_id
        assert order.status == OrderStatus.PROCESSING
        assert order.created_at == now
        assert order.updated_at == now

    def test_order_from_dict_with_missing_optional_fields(self):
        custom_id = ObjectId()
        data = {
            "_id": custom_id,
            "status": "shipped",
        }

        order = Order.from_dict(data)

        assert order.id == custom_id
        assert order.status == OrderStatus.SHIPPED
        assert isinstance(order.created_at, datetime)
        assert isinstance(order.updated_at, datetime)

    def test_order_status_transitions(self):
        order = Order(status=OrderStatus.CREATED)
        assert order.status == OrderStatus.CREATED

        order.status = OrderStatus.PROCESSING
        assert order.status == OrderStatus.PROCESSING

        order.status = OrderStatus.SHIPPED
        assert order.status == OrderStatus.SHIPPED

        order.status = OrderStatus.DELIVERED
        assert order.status == OrderStatus.DELIVERED
