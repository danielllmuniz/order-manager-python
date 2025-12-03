import pytest
from bson import ObjectId

from order_service.src.application.use_cases.get_order_use_case import GetOrderUseCase
from order_service.src.application.dtos.order_dto import GetOrderRequest
from order_service.src.domain.entities.order import Order
from order_service.src.domain.value_objects.order_status import OrderStatus
from order_service.src.domain.exceptions.order_exceptions import OrderNotFoundException


class TestGetOrderUseCase:

    def test_get_order_from_repository(self, mock_repository, mock_logger, sample_order_id):
        order = Order(status=OrderStatus.CREATED, id=sample_order_id)
        mock_repository.find_by_id.return_value = order

        use_case = GetOrderUseCase(
            order_repository=mock_repository,
            logger=mock_logger,
        )

        request = GetOrderRequest(order_id=str(sample_order_id))
        result = use_case.execute(request)

        assert result.id == str(sample_order_id)
        assert result.status == OrderStatus.CREATED.value
        mock_repository.find_by_id.assert_called_once_with(str(sample_order_id))

    def test_get_order_from_cache(self, mock_repository, mock_logger, mock_redis, sample_order_id):
        order = Order(status=OrderStatus.PROCESSING, id=sample_order_id)
        cached_order = order.to_dict()
        mock_redis.get.return_value = cached_order

        use_case = GetOrderUseCase(
            order_repository=mock_repository,
            logger=mock_logger,
            redis_repository=mock_redis,
        )

        request = GetOrderRequest(order_id=str(sample_order_id))
        result = use_case.execute(request)

        assert result.id == str(sample_order_id)
        assert result.status == OrderStatus.PROCESSING.value
        mock_redis.get.assert_called_once()
        mock_repository.find_by_id.assert_not_called()

    def test_get_order_cache_miss_then_fetch_from_repository(
        self, mock_repository, mock_logger, mock_redis, sample_order_id
    ):
        order = Order(status=OrderStatus.SHIPPED, id=sample_order_id)
        mock_redis.get.return_value = None
        mock_repository.find_by_id.return_value = order

        use_case = GetOrderUseCase(
            order_repository=mock_repository,
            logger=mock_logger,
            redis_repository=mock_redis,
        )

        request = GetOrderRequest(order_id=str(sample_order_id))
        result = use_case.execute(request)

        assert result.id == str(sample_order_id)
        assert result.status == OrderStatus.SHIPPED.value
        mock_redis.get.assert_called_once()
        mock_repository.find_by_id.assert_called_once()

    def test_get_order_not_found(self, mock_repository, mock_logger, sample_order_id):
        mock_repository.find_by_id.return_value = None

        use_case = GetOrderUseCase(
            order_repository=mock_repository,
            logger=mock_logger,
        )

        request = GetOrderRequest(order_id=str(sample_order_id))
        with pytest.raises(OrderNotFoundException):
            use_case.execute(request)
