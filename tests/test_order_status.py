import pytest

from order_service.src.domain.value_objects.order_status import OrderStatus


class TestOrderStatus:
    def test_order_status_created(self):
        status = OrderStatus.CREATED
        assert status.value == "created"

    def test_order_status_processing(self):
        status = OrderStatus.PROCESSING
        assert status.value == "processing"

    def test_order_status_shipped(self):
        status = OrderStatus.SHIPPED
        assert status.value == "shipped"

    def test_order_status_delivered(self):
        status = OrderStatus.DELIVERED
        assert status.value == "delivered"

    def test_order_status_from_string(self):
        status = OrderStatus("created")
        assert status == OrderStatus.CREATED

    def test_all_order_statuses_exist(self):
        expected_statuses = ["created", "processing", "shipped", "delivered"]
        actual_statuses = [status.value for status in OrderStatus]

        for expected in expected_statuses:
            assert expected in actual_statuses

    def test_order_status_equality(self):
        status1 = OrderStatus.CREATED
        status2 = OrderStatus.CREATED
        status3 = OrderStatus.PROCESSING

        assert status1 == status2
        assert status1 != status3
