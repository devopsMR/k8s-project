import pika
import logging
import sys
from time import sleep
import os
from prometheus_client import Counter, start_http_server

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "pc")
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", 9422))  # Default Prometheus port

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

# Prometheus message consumption counter
MESSAGE_COUNT = Counter("consumer_messages_count", "Total number of messages consumed", ["queue_name"])


def on_message(message_channel, method_frame, header_frame, body):
    """
    Callback function for processing received messages.
    """
    # Increment Prometheus counter with queue name
    MESSAGE_COUNT.labels(queue_name=RABBITMQ_QUEUE).inc()

    # Log message details
    print(f"Message Delivery Tag: {method_frame.delivery_tag}")
    print(f"Message Body: {body.decode()}")
    LOG.info('Message has been received: %s', body)

    # Acknowledge message
    message_channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    # Wait for RabbitMQ to start (ensure it's ready)
    sleep(5)

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)

    # Start Prometheus HTTP server
    LOG.info(f"Starting Prometheus HTTP server on port {PROMETHEUS_PORT}...")
    start_http_server(PROMETHEUS_PORT)

    # Define RabbitMQ connection parameters
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, virtual_host='/',
                                           credentials=credentials, client_properties={ "connection_name": "consumer"})

    # Establish connection to RabbitMQ
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    # Listen to messages using the defined callback
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=on_message)

    LOG.info(
        f"Waiting for messages on queue '{RABBITMQ_QUEUE}'. Prometheus metrics are available on port {PROMETHEUS_PORT}.")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        LOG.info("Stopping message consumption...")
        channel.stop_consuming()
    finally:
        connection.close()
