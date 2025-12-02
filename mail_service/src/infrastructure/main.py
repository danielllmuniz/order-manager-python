from mail_service.src.infrastructure.messaging.rabbitmq.mail_consumer import MailConsumer
from mail_service.src.infrastructure.messaging.rabbitmq.mail_infrastructure import MailServiceInfrastructure
from mail_service.src.infrastructure.messaging.rabbitmq.connection import RabbitMQConnection

def main():
    connection = RabbitMQConnection()
    channel = connection.create_channel()

    infra = MailServiceInfrastructure(channel)
    infra.setup()
    print(f"✓ Fila '{MailServiceInfrastructure.QUEUE_NAME}' criada/verificada")
    print(f"✓ Bindings: {MailServiceInfrastructure.BINDINGS}")

    consumer = MailConsumer(channel)

    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        print("\n✓ Parando consumer...")
        connection.close()
        print("✓ Conexão fechada")


if __name__ == "__main__":
    main()
