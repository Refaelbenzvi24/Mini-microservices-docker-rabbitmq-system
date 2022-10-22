import logging
import os
import time

import pika
from pika import BlockingConnection

logger = logging.getLogger(__name__)


class MessageBroker:
	def __init__(self):
		self.host = os.environ.get("RABBITMQ_HOST") or 'localhost'
		self.port = int(os.environ.get("RABBITMQ_PORT") or '5672')
		self.connection: BlockingConnection | None = None
	
	def __delete__(self):
		self.close_connection()
	
	@staticmethod
	def wait_for_connection():
		
		while True:
			try:
				message_broker = MessageBroker()
				message_broker.connect()
				message_broker.connection.close()
				break
			
			except Exception:
				logger.info("Waiting for message broker...")
				time.sleep(1)
				continue
	
	def connect(self):
		connection_params = pika.ConnectionParameters(host=self.host, port=self.port)
		connection = pika.BlockingConnection(connection_params)
		self.connection = connection
		return connection.channel()
	
	def close_connection(self):
		if self.connection:
			self.connection.close()


class Producer:
	def __init__(self, queue: str, exchange=""):
		self.exchange = exchange
		self.message_broker = MessageBroker()
		self.queue = queue
		self.channel = self.message_broker.connect()
		self.channel.queue_declare(queue)
	
	def publish(self, body):
		self.channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=body)
		logger.info(f" [x] Sent message to '{self.queue}' queue")


class Consumer:
	def __init__(self, queue: str):
		self.message_broker = MessageBroker()
		self.channel = self.message_broker.connect()
		result = self.channel.queue_declare(queue=queue)
		self.queue = result.method.queue
	
	def subscribe(self, callback):
		self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
		
		logger.info(f"started consuming messages from '{self.queue}' queue")
		self.channel.start_consuming()
