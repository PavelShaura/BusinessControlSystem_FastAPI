import json

import aio_pika
from src.core.config import settings


class RabbitMQProducer:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@{settings.RABBITMQ_HOST}/"
        )
        self.channel = await self.connection.channel()

    async def publish(self, queue_name: str, message: dict):
        if not self.connection or self.connection.is_closed:
            await self.connect()

        await self.channel.declare_queue(queue_name, durable=True)
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key=queue_name
        )

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()