import pytest
from unittest.mock import MagicMock
from bson import ObjectId

from order_service.src.application.use_cases.change_order_status_use_case import ChangeOrderStatusUseCase
from order_service.src.domain.entities.order import Order
from order_service.src.domain.value_objects.order_status import OrderStatus
from order_service.src.domain.exceptions.order_exceptions import OrderNotFoundException


class TestChangeOrderStatusUseCase:

    def test_change_order_status_successfully(self, mock_repository, mock_publisher, mock_logger, sample_order_id):
        order = Order(status=OrderStatus.CREATED, id=sample_order_id)
        mock_repository.find_by_id.return_value = order

        use_case = ChangeOrderStatusUseCase(
            order_repository=mock_repository,
            order_publisher=mock_publisher,
            logger=mock_logger,
        )

        result = use_case.execute(str(sample_order_id))

        assert result.status == OrderStatus.PROCESSING.value
        mock_repository.update_status.assert_called_once()
        mock_publisher.publish_order_updated.assert_called_once()

    def test_change_order_status_with_cache_invalidation(
        self, mock_repository, mock_publisher, mock_logger, mock_redis, sample_order_id
    ):
        order = Order(status=OrderStatus.CREATED, id=sample_order_id)
        mock_repository.find_by_id.return_value = order

        use_case = ChangeOrderStatusUseCase(
            order_repository=mock_repository,
            order_publisher=mock_publisher,
            logger=mock_logger,
            redis_repository=mock_redis,
        )

        use_case.execute(str(sample_order_id))

        cache_key = f"order:{sample_order_id}"
        mock_redis.delete.assert_called_once_with(cache_key)

    def test_change_order_status_publishes_event(
        self, mock_repository, mock_publisher, mock_logger, sample_order_id
    ):
        order = Order(status=OrderStatus.CREATED, id=sample_order_id)
        mock_repository.find_by_id.return_value = order

        use_case = ChangeOrderStatusUseCase(
            order_repository=mock_repository,
            order_publisher=mock_publisher,
            logger=mock_logger,
        )

        use_case.execute(str(sample_order_id))

        mock_publisher.publish_order_updated.assert_called_once_with(
            str(sample_order_id), OrderStatus.PROCESSING.value
        )

    def test_change_order_status_order_not_found(self, mock_repository, mock_logger, sample_order_id):
        mock_repository.find_by_id.return_value = None

        use_case = ChangeOrderStatusUseCase(
            order_repository=mock_repository,
            order_publisher=MagicMock(),
            logger=mock_logger,
        )

        with pytest.raises(OrderNotFoundException):
            use_case.execute(str(sample_order_id))

    def test_change_order_status_logs_info(self, mock_repository, mock_publisher, mock_logger, sample_order_id):
        order = Order(status=OrderStatus.CREATED, id=sample_order_id)
        mock_repository.find_by_id.return_value = order

        use_case = ChangeOrderStatusUseCase(
            order_repository=mock_repository,
            order_publisher=mock_publisher,
            logger=mock_logger,
        )

        use_case.execute(str(sample_order_id))

        assert mock_logger.info.call_count >= 1
