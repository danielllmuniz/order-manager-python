from flask import Blueprint, jsonify, request
from order_service.src.infrastructure.api.composer.order_creator_composer import order_creator_composer
from order_service.src.infrastructure.api.errors.error_handler import handle_errors
from order_service.src.infrastructure.logging.config import LoggingConfig
from order_service.src.infrastructure.logging.python_logger import PythonLogger

# Setup logging
logging_config = LoggingConfig()
logging_config.setup_logging()
logger = PythonLogger(__name__)

order_route_bp = Blueprint('orders_routes', __name__, url_prefix='/')

@order_route_bp.route('/orders', methods=['POST'])
def create_orders():
    logger.info(f"POST /orders request received from {request.remote_addr}")
    try:
        logger.debug("Composing order creator dependencies")
        controller = order_creator_composer()

        logger.debug("Executing order creation controller")
        http_response = controller.handle()

        logger.info(f"Order created successfully - Status: {http_response.status_code}")
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        logger.error(f"Error creating order: {type(e).__name__} - {str(e)}")
        http_response = handle_errors(e)
        logger.warning(f"Returning error response - Status: {http_response.status_code}")
        return jsonify(http_response.body), http_response.status_code
