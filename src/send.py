import os
from aio_pika import Message, connect
from dotenv import load_dotenv


load_dotenv()

url = os.getenv('CLOUDAMQP_URL')


class RabbitMQManager:
    def __init__(self, url):
        self.url = url
        self.connection = None
        self.channel = None
        self.queue = None

    async def __aenter__(self):
        self.connection = await connect(self.url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue("0")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.connection:
            await self.connection.close()


async def send_message(command, body):
    async with RabbitMQManager(url) as channel:
        try:
            message = Message(
                body,
                headers={"command": command},
            )
            await channel.channel.default_exchange.publish(
                message,
                routing_key="0",
            )
        except Exception as e:
            print(f"Error sending command: {e}")
