from order_service.src.infrastructure.database.mongodb.connection import mongo_connection
from order_service.src.infrastructure.database.mongodb.order_repository import OrderRepository
from order_service.src.infrastructure.cache.redis.connection import redis_connection
from order_service.src.infrastructure.cache.redis.redis_repository import RedisRepository
from order_service.src.infrastructure.logging.config import LoggingConfig
from order_service.src.infrastructure.logging.python_logger import PythonLogger
from order_service.src.application.use_cases.get_order_use_case import GetOrderUseCase


def order_getter_composer():
    logging_config = LoggingConfig()
    logging_config.setup_logging()
    logger = PythonLogger(__name__)

    database = OrderRepository(mongo_connection, logger)
    cache = RedisRepository(redis_connection, logger)

    usecase = GetOrderUseCase(
        database,
        logger,
        cache
    )

    return usecase, logger
