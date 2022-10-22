import logging
import json
import os
import re

import fileSystemHelper
from messageBroker import MessageBroker, Consumer, Producer

PATH_TO_SEARCH_IN = "./theHarvester"
KEYWORD_TO_SEARCH_FOR = 'password: '
FILE_EXTENSIONS_TO_SEARCH_IN = ['', '.py', '.txt', '.yml', '.md', '.yaml', '.json', '.ini', '.lock', '.cfg']

logging.basicConfig(level=logging.INFO)
logging.getLogger("pika").propagate = False
logger = logging.getLogger(__name__)


def password_producer(password: str):
	producer = Producer("controller_queue")
	message = json.dumps({"password": password})
	producer.publish(body=message)


def search_for_keyword_in_file(keyword: str, file: str, directory: str) -> str | None:
	with open(rf'{directory}/{file}', 'r') as file:
		file_content = file.read()
		
		if keyword in file_content:
			return file_content


def search_for_password():
	"""
	Searches for password in theharvester directory and send the result to the password_producer.
	"""
	files_list = fileSystemHelper.list_nested_files_in_path(PATH_TO_SEARCH_IN)
	
	for file_object in files_list:
		file_name, file_extension = os.path.splitext(file_object['file'])
		
		if file_extension in FILE_EXTENSIONS_TO_SEARCH_IN:
			file_search_result = search_for_keyword_in_file(KEYWORD_TO_SEARCH_FOR, file_object['file'], file_object['directory'])
			
			if file_search_result:
				search_result = re.split('[ ]|\n', file_search_result.split(KEYWORD_TO_SEARCH_FOR)[1])[0]
				password_producer(search_result)
				break


def password_consumer():
	consumer = Consumer('password_queue')
	
	def callback(channel, method, properties, body):
		logger.info("Got a message from 'password_queue'")
		search_for_password()
	
	consumer.subscribe(callback)


if __name__ == '__main__':
	logger.info("Password module is listening...")
	MessageBroker.wait_for_connection()
	password_consumer()
