import asyncio
import os
import aiohttp

from multiprocessing import Process
from aio_pika.abc import AbstractIncomingMessage
from dotenv import load_dotenv
from src.bot import app
from src.send import RabbitMQManager

load_dotenv()


async def on_message(message: AbstractIncomingMessage) -> None:

    global last_received_message
    command = message.headers.get("command")

    if command not in ["print", "send"]:
        last_received_message = message.body

    if command == 'print':
        try:
            print(100 * "*", "\nExecuting command: print\nLast message:", last_received_message.decode('utf-8'))
        except Exception as e:
            print(f"No messages in the queue {e}")

    elif command == 'send':
        try:
            await send_to_external_api(last_received_message)
        except Exception as e:
            print(f"No messages in the queue {e}")
    else:
        print(100 * "*", "\nMessage body is: %r" % message.body.decode('utf-8'))


async def send_to_external_api(message):
    message_text = message.decode('utf-8')

    async with aiohttp.ClientSession() as session:
        payload = {"message": message_text}
        print("Payload: ", payload)
        async with session.post(os.getenv('EXTERNAL_API_URL'), json=payload) as response:
            if response.status == 200:
                print("Message successfully sent to the external API", payload)
            else:
                print(f"Error sending message to the external API. Status code: {response.status}")


async def listening_queue():
    async with RabbitMQManager(os.getenv('CLOUDAMQP_URL')) as manager:
        try:
            await manager.queue.consume(on_message, no_ack=True)
            print(" [*] Waiting for messages. To exit press CTRL+C")

            await asyncio.Future()

        except Exception as e:
            print(f"Error sending command: {e}")


def run_telegram():
    app.run_polling()


def run_listening_queue():
    asyncio.run(listening_queue())


def main():
    telegram_process = Process(target=run_telegram)
    listening_queue_process = Process(target=run_listening_queue)

    telegram_process.start()
    listening_queue_process.start()

    telegram_process.join()
    listening_queue_process.join()


if __name__ == "__main__":
    last_received_message = None
    main()
