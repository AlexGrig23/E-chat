# Telegram bot (E-chat)
Telegram bot with RabbitMQ

## Description

This app created with used cloud service RabbitMQ 
https://crow.rmq.cloudamqp.com/
credentionals you will find in .env file if you want check working queue in RabbitMQ interface
AMQP_USER
AMQP_PASSWORD

Docker-compose file settings according to technical specefication but it's have some comments


For quick activation, you can also use the credentials for the telegram bot that are in the .env file,
Bot name: @rabbitmq_test_bot

---
## Installation
**1. Clone the repository:**

   ```shell
   git clone https://github.com/AlexGrig23/e-chat.git
   ```

  Create virtual env.

   ```shell
   python -m venv venv
   ```
Don't forget to activate it cd venv/Scripts
"\.activate" and come back in workdir e-chat

**2. Create a `.env` file based on the `.env.example` file:**

   ```shell
   cd e-chat
   ```

   ```shell
   copy .env.example .env
   ```
**3. If you want to run using Docker you must have a Docker desktop**
  
   ```shell
   docker compose build --no-cache
   ```
   
   After that, you must run next command, It builds the images if they are not located locally and starts the containers:

   ```shell
   docker compose up
   ```

After that, the application starts automatically namely, 
the bot will be launched and queue listening will be enabled.
You'll see command in terminal "Application started" 
After that you can write command /start in TG bot, 
then you can write message and check works consume and message handler
in terminal IDE

	

  
