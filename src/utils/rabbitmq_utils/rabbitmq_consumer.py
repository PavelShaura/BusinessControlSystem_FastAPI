import json

from aio_pika import connect_robust, IncomingMessage

from src.core.config import settings
from worker.notify import send_invite_email_task


class RabbitMQConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = 'email_tasks'

    async def connect(self):
        self.connection = await connect_robust(
            f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@{settings.RABBITMQ_HOST}/"
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

    async def consume(self):
        await self.connect()
        queue = await self.channel.declare_queue(self.queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                print(message)
                await self.process_message(message)

    async def process_message(self, message: IncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())
            if body['task'] == 'send_invite_email':
                email, invite_token = body['args']
                # Вызываем Celery задачу
                send_invite_email_task.delay(email, invite_token)
            else:
                print(f"Unknown task: {body['task']}")



