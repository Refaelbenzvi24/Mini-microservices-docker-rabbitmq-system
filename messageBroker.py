import pika
import os
import time

from pika.exceptions import AMQPConnectionError

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST") or 'localhost'
RABBITMQ_PORT = int(os.environ.get("RABBITMQ_PORT") or '5672')


class MessageBroker:
	def __init__(self):
		self.connection_params = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
		self.connection: pika.BlockingConnection | None = None
		self.test_connection()
	
	def __delete__(self):
		self.close_connection()
	
	def test_connection(self):
		
		while True:
			try:
				pika.BlockingConnection(self.connection_params).close()
				break
			except AMQPConnectionError:
				print("Waiting for RabbitMQ to start...")
				time.sleep(5)
	
	def get_connection(self):
		if self.connection is None:
			self.connection = pika.BlockingConnection(self.connection_params)
			return self.connection
		
		return self.connection
	
	def close_connection(self):
		if self.connection:
			self.connection.close()


class Producer:
	__message_broker: MessageBroker | None = None
	connection: pika.BlockingConnection | None = None
	
	def __init__(self, queue: str, exchange=""):
		if Producer.__message_broker is None:
			Producer.__message_broker = MessageBroker()
		self.exchange = exchange
		self.queue = queue
		
		if self.connection is None:
			Producer.connection = Producer.__message_broker.get_connection()
		
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue=self.queue, durable=True)
	
	def publish(self, body):
		self.channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=body)
		print(f" [x] Sent message to '{self.queue}' queue")


class Consumer:
	__message_broker: MessageBroker | None = None
	connection: pika.BlockingConnection | None = None
	
	def __init__(self, queue: str, exchange=""):
		if Consumer.__message_broker is None:
			Consumer.__message_broker = MessageBroker()
		self.exchange = exchange
		self.queue = queue
		
		if self.connection is None:
			Consumer.connection = Consumer.__message_broker.get_connection()
		
		self.channel = self.connection.channel()
		
		self.channel.queue_declare(queue=self.queue)
	
	def subscribe(self, callback):
		self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
		print(f"Subscribing for messages from '{self.queue}' queue")
		self.channel.start_consuming()
