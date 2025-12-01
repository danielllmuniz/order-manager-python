from src.infrastructure.messaging.rabbitmq.connection import RabbitMQConnection
from src.infrastructure.messaging.rabbitmq.order_infrastructure import OrderServiceInfrastructure
from src.infrastructure.messaging.rabbitmq.order_publisher import OrderPublisher

def main():
    # Conexão
    connection = RabbitMQConnection()
    channel = connection.create_channel()

    # Setup da infraestrutura (exchange)
    infra = OrderServiceInfrastructure(channel)
    infra.setup()
    print(f"✓ Exchange '{OrderServiceInfrastructure.EXCHANGE_NAME}' criada/verificada")

    # Publisher
    publisher = OrderPublisher(channel)

    # Exemplo de publicação
    publisher.publish_order_created(
        order_id="order-123",
        customer_email="cliente@email.com",
        total=199.90
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
