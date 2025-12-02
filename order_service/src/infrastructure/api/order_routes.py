from flask import Blueprint, jsonify
from order_service.src.infrastructure.api.composer.order_creator_composer import order_creator_composer
from order_service.src.infrastructure.api.errors.error_handler import handle_errors

order_route_bp = Blueprint('orders_routes', __name__, url_prefix='/')

@order_route_bp.route('/orders', methods=['POST'])
def create_orders():
    try:

        controller = order_creator_composer()
        http_response = controller.handle()
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code
