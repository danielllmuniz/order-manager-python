import pytest
from unittest.mock import MagicMock
from bson import ObjectId

from order_service.src.application.ports.logger import ILogger
from order_service.src.domain.interfaces.order_repository import IOrderRepository
from order_service.src.domain.interfaces.order_publisher import IOrderPublisher
from order_service.src.domain.interfaces.redis_repository import IRedisRepository


@pytest.fixture
def mock_logger():
    logger = MagicMock(spec=ILogger)
    return logger


@pytest.fixture
def mock_repository():
    repository = MagicMock(spec=IOrderRepository)
    return repository


@pytest.fixture
def mock_publisher():
    publisher = MagicMock(spec=IOrderPublisher)
    return publisher


@pytest.fixture
def mock_redis():
    redis = MagicMock(spec=IRedisRepository)
    return redis


@pytest.fixture
def sample_order_id():
    return ObjectId()
