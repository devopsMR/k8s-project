import pika
import logging
import sys
from time import sleep, strftime
from pika.exceptions import UnroutableError
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "pc")
RABBITMQ_MESSAGE_REPEAT = os.getenv("RABBITMQ_MESSAGE_REPEAT", "0")  # Defaults to 0 (infinite)
RABBITMQ_MESSAGE = os.getenv("RABBITMQ_MESSAGE")

# Validate required environment variables
if not RABBITMQ_HOST:
    print("Missing required environment variable: RABBITMQ_HOST")
    sys.exit(1)

if not RABBITMQ_PORT:
    print("Missing required environment variable: RABBITMQ_PORT")
    sys.exit(1)

if not RABBITMQ_USERNAME:
    print("Missing required environment variable: RABBITMQ_USERNAME")
    sys.exit(1)

if not RABBITMQ_PASSWORD:
    print("Missing required environment variable: RABBITMQ_PASSWORD")
    sys.exit(1)


if __name__ == '__main__':
    # Wait for RabbitMQ to be ready
    sleep(5)

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)

    # Define RabbitMQ connection parameters
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(RABBITMQ_HOST, RABBITMQ_PORT, '/',
                                           credentials, client_properties={ "connection_name": "producer"})

    # Establish connection to RabbitMQ
    connection = pika.BlockingConnection(parameters)
    try:
        # Create a communication channel
        channel = connection.channel()

        # Declare a queue
        channel.queue_declare(queue=RABBITMQ_QUEUE)

        # Enable delivery confirmations
        channel.confirm_delivery()

        counter = 1  # Message counter

        # Infinite if repeat is 0
        while int(RABBITMQ_MESSAGE_REPEAT) == 0 or counter <= int(RABBITMQ_MESSAGE_REPEAT):
            current_time = strftime("%Y-%m-%d %H:%M:%S")

            # Use RABBITMQ_MESSAGE if provided, otherwise default to auto-generated message
            message = os.getenv("RABBITMQ_MESSAGE")

            if not message:  # Handles both missing (`None`) and empty (`""`) cases
                message = "Hello today date is {} time is {} this is message number {}".format(
                    current_time.split()[0], current_time.split()[1], counter
                )

            try:
                channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=message, mandatory=True)
                LOG.info('Message has been delivered: %s', message)
            except UnroutableError:
                LOG.warning('Message NOT delivered: %s', message)

            counter += 1
            sleep(20)

    finally:
        # Close the connection to RabbitMQ
        connection.close()
