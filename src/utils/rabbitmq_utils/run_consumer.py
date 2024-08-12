import asyncio

from src.utils.rabbitmq_utils.rabbitmq_consumer import RabbitMQConsumer


async def run_consumer():
    consumer = RabbitMQConsumer()
    await consumer.consume()

if __name__ == "__main__":
    asyncio.run(run_consumer())