import logging
import json

import fileSystemHelper
from messageBroker import MessageBroker, Consumer, Producer

JSON_OUTPUT_PATH = fileSystemHelper.get_full_path(relative_path="./output/result.json")

logging.basicConfig(level=logging.INFO)
logging.getLogger("pika").propagate = False
logger = logging.getLogger(__name__)



def generate_json_output(body: dict):
	"""
	Generates the json file for the consumed messages.
	"""
	if "password" in body:
		json_output_file = fileSystemHelper.read_json_file(JSON_OUTPUT_PATH)
		json_output_file["password"] = body["password"]
		fileSystemHelper.write_to_json_file(json_output_file, JSON_OUTPUT_PATH)
	if "files_types" in body:
		json_output_file = fileSystemHelper.read_json_file(JSON_OUTPUT_PATH)
		json_output_file["files_types"] = body["files_types"]
		fileSystemHelper.write_to_json_file(json_output_file, JSON_OUTPUT_PATH)


def controller_consumer():
	consumer = Consumer('controller_queue')
	
	def callback(channel, method, properties, body):
		logger.info("received new message from 'controller_queue'")
		json_body = json.loads(body)
		generate_json_output(json_body)
	
	consumer.subscribe(callback)


def analyze_producer():
	producer = Producer("analyze_queue")
	producer.publish(body="Trigger analyze")


def password_producer():
	producer = Producer("password_queue")
	producer.publish(body="Trigger password")


if __name__ == '__main__':
	logger.info("Controller module is running and listening...")
	
	fileSystemHelper.write_to_json_file({}, JSON_OUTPUT_PATH)
	MessageBroker.wait_for_connection()
	password_producer()
	analyze_producer()
	controller_consumer()
