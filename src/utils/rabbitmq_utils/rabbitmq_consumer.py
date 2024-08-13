import asyncio
import json

from aio_pika import connect_robust, IncomingMessage
from aiormq import ChannelInvalidStateError
from celery.result import AsyncResult

from src.core.config import settings
from worker.celery_tasks_factory.tasks_factory import TaskFactory


class RabbitMQConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.task_factory = TaskFactory()

    async def connect(self):
        self.connection = await connect_robust(
            f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@{settings.RABBITMQ_HOST}/"
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

    async def consume(self, queue_names):
        while True:
            try:
                await self.connect()
                tasks = []
                for queue_name in queue_names:
                    tasks.append(asyncio.create_task(self.consume_queue(queue_name)))
                await asyncio.gather(*tasks)
            except ChannelInvalidStateError as e:
                print(f"Channel closed with error: {e}, reconnecting...")
                await asyncio.sleep(5)  # Задержка перед повторным подключением
            except asyncio.CancelledError:
                print("Task was cancelled")
                raise  # Передаем исключение дальше для корректного завершения

    async def consume_queue(self, queue_name):
        try:
            queue = await self.channel.declare_queue(queue_name, durable=True)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        print(f"Received message from {queue_name}")
                        await self.process_message(message)
                    except Exception as e:
                        print(f"Failed to process message: {e}")
                        await message.reject(requeue=True)
        except ChannelInvalidStateError:
            print(f"Channel for queue {queue_name} was closed unexpectedly.")

    async def process_message(self, message: IncomingMessage):
        async with message.process():
            try:
                body = json.loads(message.body.decode())
                task_type = body["task_type"]
                task_args = body["task_args"]

                task = self.task_factory.create_task(task_type)
                result = await task.execute(**task_args)

                if isinstance(result, AsyncResult):
                    if result.state in ["PENDING", "SUCCESS"]:
                        print("Task successfully delivered to Celery")
                    else:
                        print(f"Task failed in Celery with state: {result.state}")
                        raise Exception("Task execution failed in Celery")
                else:
                    print("Task executed without AsyncResult, assuming success.")

            except Exception as e:
                print(f"Failed to process message: {e}")
                raise
