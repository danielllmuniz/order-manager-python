from order_service.src.infrastructure.database.mongodb.connection import mongo_connection
from order_service.src.infrastructure.database.mongodb.order_repository import OrderRepository
from order_service.src.infrastructure.cache.redis.connection import redis_connection
from order_service.src.infrastructure.cache.redis.redis_repository import RedisRepository
from order_service.src.infrastructure.messaging.rabbitmq.connection import rabbitmq_connection
from order_service.src.infrastructure.messaging.rabbitmq.order_publisher import OrderPublisher
from order_service.src.infrastructure.logging.config import LoggingConfig
from order_service.src.infrastructure.logging.python_logger import PythonLogger
from order_service.src.application.use_cases.create_order_use_case import CreateOrderUseCase
from order_service.src.infrastructure.api.controller.order_creator_controller import OrderCreatorController

def order_creator_composer():
    # Setup logging
    logging_config = LoggingConfig()
    logging_config.setup_logging()
    logger = PythonLogger(__name__)

    database = OrderRepository(mongo_connection, logger)
    cache = RedisRepository(redis_connection, logger)
    messaging = OrderPublisher(rabbitmq_connection, logger)

    usecase = CreateOrderUseCase(
        database,
        messaging,
        logger,
        cache
    )

    controller = OrderCreatorController(usecase)

    return controller
