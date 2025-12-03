import pytest
from bson import ObjectId

from order_service.src.application.use_cases.create_order_use_case import CreateOrderUseCase
from order_service.src.domain.value_objects.order_status import OrderStatus


class TestCreateOrderUseCase:

    def test_create_order_successfully(self, mock_repository, mock_publisher, mock_logger, sample_order_id):
        mock_repository.create.return_value = sample_order_id

        use_case = CreateOrderUseCase(
            order_repository=mock_repository,
            order_publisher=mock_publisher,
            logger=mock_logger,
        )

        result = use_case.execute()

        assert result.status == OrderStatus.CREATED.value
        assert result.id == str(sample_order_id)
        mock_repository.create.assert_called_once()
        mock_publisher.publish_order_created.assert_called_once_with(str(sample_order_id))
        mock_logger.info.assert_called()

    def test_create_order_with_cache(self, mock_repository, mock_publisher, mock_logger, mock_redis, sample_order_id):
        mock_repository.create.return_value = sample_order_id

        use_case = CreateOrderUseCase(
            order_repository=mock_repository,
            order_publisher=mock_publisher,
            logger=mock_logger,
            redis_repository=mock_redis,
        )

        result = use_case.execute()

        assert result.status == OrderStatus.CREATED.value
        assert result.id == str(sample_order_id)
        mock_redis.set.assert_called_once()
        cache_key = f"order:{sample_order_id}"
        call_args = mock_redis.set.call_args
        assert call_args[0][0] == cache_key
        assert call_args[1]["ttl"] == 3600

    def test_create_order_publishes_event(self, mock_repository, mock_publisher, mock_logger, sample_order_id):
        mock_repository.create.return_value = sample_order_id

        use_case = CreateOrderUseCase(
            order_repository=mock_repository,
            order_publisher=mock_publisher,
            logger=mock_logger,
        )

        use_case.execute()

        mock_publisher.publish_order_created.assert_called_once_with(str(sample_order_id))

    def test_create_order_logs_info(self, mock_repository, mock_publisher, mock_logger, sample_order_id):
        mock_repository.create.return_value = sample_order_id

        use_case = CreateOrderUseCase(
            order_repository=mock_repository,
            order_publisher=mock_publisher,
            logger=mock_logger,
        )

        use_case.execute()

        assert mock_logger.info.call_count >= 2
