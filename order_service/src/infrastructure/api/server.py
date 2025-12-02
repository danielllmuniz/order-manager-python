from flask import Flask
from order_service.src.infrastructure.database.mongodb.connection import mongo_connection
from order_service.src.infrastructure.cache.redis.connection import redis_connection
from order_service.src.infrastructure.messaging.rabbitmq.connection import rabbitmq_connection
from order_service.src.infrastructure.api.order_routes import order_route_bp
mongo_connection.connect()
redis_connection.connect()
rabbitmq_connection.connect()

app = Flask(__name__)



@app.route('/health', methods=['GET'])
def health():
    return {
        'status': 'healthy',
        'service': 'audit-manager-application-service'
    }, 200

app.register_blueprint(order_route_bp)
