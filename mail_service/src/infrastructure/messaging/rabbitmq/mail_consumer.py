import json
import pika
from mail_service.src.infrastructure.messaging.rabbitmq.mail_infrastructure import MailServiceInfrastructure


class MailConsumer:
    def __init__(self, channel: pika.channel.Channel) -> None:
        self._channel = channel
        self._queue = MailServiceInfrastructure.QUEUE_NAME

    def start_consuming(self) -> None:
        self._channel.basic_qos(prefetch_count=1)

        self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=self._handle_message
        )

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
 
            print(f"📨 Recebido: {event}")

            if event == "order_created":
                self._send_order_confirmation(message)
            elif event == "order_cancelled":
                self._send_cancellation_email(message)
            else:
                print(f"⚠ Evento desconhecido: {event}")

            channel.basic_ack(delivery_tag=method.delivery_tag)

        except json.JSONDecodeError as e:
            print(f"✗ Erro ao decodificar mensagem: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        except Exception as e:
            print(f"✗ Erro ao processar mensagem: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def _send_order_confirmation(self, message: dict) -> None:
        email = message.get("customer_email")
        order_id = message.get("order_id")
        total = message.get("total")

        print(f"  ✉ Enviando confirmação para {email}")
        print(f"    Pedido: {order_id} | Total: R$ {total}")

    def _send_cancellation_email(self, message: dict) -> None:
        order_id = message.get("order_id")
        reason = message.get("reason")

        print(f"  ✉ Enviando email de cancelamento")
        print(f"    Pedido: {order_id} | Motivo: {reason}")
