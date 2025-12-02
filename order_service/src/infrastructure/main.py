from order_service.src.infrastructure.messaging.rabbitmq.connection import RabbitMQConnection
from order_service.src.infrastructure.messaging.rabbitmq.order_infrastructure import OrderServiceInfrastructure
from order_service.src.infrastructure.messaging.rabbitmq.order_publisher import OrderPublisher

def main():
    connection = RabbitMQConnection()
    channel = connection.create_channel()

    infra = OrderServiceInfrastructure(channel)
    infra.setup()
    print(f"✓ Exchange '{OrderServiceInfrastructure.EXCHANGE_NAME}' criada/verificada")

    publisher = OrderPublisher(channel)

    publisher.publish_order_created(
        order_id="order-123",
    )
    print("✓ Evento 'orders.created' publicado")

    publisher.publish_order_updated(
        order_id="order-123",
        status="processing"
    )
    print("✓ Evento 'orders.updated' publicado")

    connection.close()
    print("✓ Conexão fechada")


if __name__ == "__main__":
    main()
