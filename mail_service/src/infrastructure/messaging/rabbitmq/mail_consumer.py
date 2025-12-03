import json
import pika
from mail_service.src.infrastructure.messaging.rabbitmq.mail_infrastructure import MailServiceInfrastructure
from order_service.src.infrastructure.logging.config import LoggingConfig
from order_service.src.infrastructure.logging.python_logger import PythonLogger

# Setup logging
logging_config = LoggingConfig()
logging_config.setup_logging()
logger = PythonLogger(__name__)


class MailConsumer:
    def __init__(self, channel: pika.channel.Channel) -> None:
        self._channel = channel
        self._queue = MailServiceInfrastructure.QUEUE_NAME

    def start_consuming(self) -> None:
        logger.info(f"Starting mail consumer for queue: {self._queue}")
        self._channel.basic_qos(prefetch_count=1)

        self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=self._handle_message
        )

        logger.info(f"Waiting for messages in '{self._queue}'...")
        print(f"✓ Aguardando mensagens em '{self._queue}'...")
        self._channel.start_consuming()

    def _handle_message(
        self,
        channel: pika.channel.Channel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
    ) -> None:
        try:
            message = json.loads(body)
            event = message.get("event")

            logger.info(f"Message received: {event}")
            print(f"📨 Recebido: {event}")

            if event == "order_created":
                self._send_order_confirmation(message)
            elif event == "order_updated":
                self._send_order_update_email(message)
            elif event == "order_cancelled":
                self._send_cancellation_email(message)
            else:
                logger.warning(f"Unknown event type: {event}")
                print(f"⚠ Evento desconhecido: {event}")

            channel.basic_ack(delivery_tag=method.delivery_tag)
            logger.debug(f"Message acknowledged: {event}")

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding message: {str(e)}")
            print(f"✗ Erro ao decodificar mensagem: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        except Exception as e:
            logger.error(f"Error processing message: {type(e).__name__} - {str(e)}")
            print(f"✗ Erro ao processar mensagem: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def _send_order_confirmation(self, message: dict) -> None:
        email = message.get("customer_email")
        order_id = message.get("order_id")
        total = message.get("total")

        logger.info(f"Sending order confirmation email to {email}")
        print(f"  ✉ Enviando confirmação para {email}")
        print(f"    Pedido: {order_id} | Total: R$ {total}")

    def _send_order_update_email(self, message: dict) -> None:
        order_id = message.get("order_id")
        status = message.get("status")

        logger.info(f"Sending order update email for order {order_id} with status {status}")
        print("  ✉ Enviando email de atualização de pedido")
        print(f"    Pedido: {order_id} | Novo Status: {status}")

    def _send_cancellation_email(self, message: dict) -> None:
        order_id = message.get("order_id")
        reason = message.get("reason")

        logger.info(f"Sending order cancellation email for order {order_id}")
        print("  ✉ Enviando email de cancelamento")
        print(f"    Pedido: {order_id} | Motivo: {reason}")
