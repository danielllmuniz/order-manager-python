from flask import Flask
from order_service.src.infrastructure.database.mongodb.connection import mongo_connection
from order_service.src.infrastructure.cache.redis.connection import redis_connection
from order_service.src.infrastructure.messaging.rabbitmq.connection import rabbitmq_connection
from order_service.src.infrastructure.api.order_routes import order_route_bp
from order_service.src.infrastructure.logging.config import LoggingConfig
from order_service.src.infrastructure.logging.python_logger import PythonLogger

logging_config = LoggingConfig()
logging_config.setup_logging()
logger = PythonLogger(__name__)

logger.info("Initializing application...")

logger.info("Connecting to MongoDB...")
mongo_connection.connect()
logger.info("MongoDB connected successfully")

logger.info("Connecting to Redis...")
redis_connection.connect()
logger.info("Redis connected successfully")

logger.info("Connecting to RabbitMQ...")
rabbitmq_connection.connect()
logger.info("RabbitMQ connected successfully")

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    logger.debug("Health check endpoint called")
    return {
        'status': 'healthy',
        'service': 'audit-manager-application-service'
    }, 200

app.register_blueprint(order_route_bp)

logger.info("Application initialized successfully")
