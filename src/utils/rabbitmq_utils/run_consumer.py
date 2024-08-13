import asyncio

from src.utils.rabbitmq_utils.rabbitmq_consumer import RabbitMQConsumer
from src.core.config import settings


async def run_consumer():
    consumer = RabbitMQConsumer()
    queue_names = [
        settings.RMQ_SEND_MAIL_QUEUE,
        settings.RMQ_REBIND_MAIL_QUEUE,
        settings.RMQ_INVITE_EMPLOYEE_MAIL_QUEUE,
    ]
    await consumer.consume(queue_names)


if __name__ == "__main__":
    try:
        print("Consumer starting ...")
        asyncio.run(run_consumer())
    except Exception as e:
        print(f"Consumer failed: {e}")
