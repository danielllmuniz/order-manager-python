from flask import Blueprint, jsonify, request
from order_service.src.infrastructure.api.composer.order_creator_composer import order_creator_composer
from order_service.src.infrastructure.api.composer.order_getter_composer import order_getter_composer
from order_service.src.infrastructure.api.composer.order_status_changer_composer import order_status_changer_composer
from order_service.src.infrastructure.api.controller.http_types.http_request import HttpRequest
from order_service.src.infrastructure.api.controller.get_order_controller import GetOrderController
from order_service.src.infrastructure.api.controller.change_order_status_controller import ChangeOrderStatusController
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

@order_route_bp.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id: str):
    logger.info(f"GET /orders/{order_id} request received from {request.remote_addr}")
    try:
        logger.debug("Composing order getter dependencies")
        usecase, getter_logger = order_getter_composer()
        controller = GetOrderController(usecase, getter_logger)

        logger.debug("Executing order getter controller")
        http_request = HttpRequest(param={"order_id": order_id})
        http_response = controller.handle(http_request)

        logger.info(f"Order fetched successfully - Status: {http_response.status_code}")
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        logger.error(f"Error fetching order: {type(e).__name__} - {str(e)}")
        http_response = handle_errors(e)
        logger.warning(f"Returning error response - Status: {http_response.status_code}")
        return jsonify(http_response.body), http_response.status_code

@order_route_bp.route('/orders/<order_id>/status', methods=['PATCH'])
def change_order_status(order_id: str):
    logger.info(f"PATCH /orders/{order_id}/status request received from {request.remote_addr}")
    try:
        logger.debug("Composing order status changer dependencies")
        usecase, changer_logger = order_status_changer_composer()
        controller = ChangeOrderStatusController(usecase, changer_logger)

        logger.debug("Executing order status changer controller")
        http_request = HttpRequest(param={"order_id": order_id})
        http_response = controller.handle(http_request)

        logger.info(f"Order status changed successfully - Status: {http_response.status_code}")
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        logger.error(f"Error changing order status: {type(e).__name__} - {str(e)}")
        http_response = handle_errors(e)
        logger.warning(f"Returning error response - Status: {http_response.status_code}")
        return jsonify(http_response.body), http_response.status_code
