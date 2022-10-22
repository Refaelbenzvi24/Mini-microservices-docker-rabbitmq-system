import logging
import os
import json
import typing
import numbers

import fileSystemHelper
from messageBroker import MessageBroker, Consumer, Producer

PATH_TO_SEARCH_IN = "./theHarvester"

logging.basicConfig(level=logging.INFO)
logging.getLogger("pika").propagate = False
logger = logging.getLogger(__name__)


def send_analyze_message(files_types):
	producer = Producer("controller_queue")
	message = json.dumps({"files_types": files_types})
	producer.publish(body=message)


def file_types_counter(files_list: list) -> {str, int}:
	"""
	Counts the amount of each file type in a give list of files.
	"""
	file_types = {}
	
	for file_object in files_list:
		file_name, file_extension = os.path.splitext(file_object['file'])
		
		if file_extension == '':
			if file_name in file_types:
				file_types[file_name] += 1
				continue
			
			file_types[file_name] = 1
			continue
		
		if file_extension in file_types:
			file_types[file_extension] += 1
			continue
		
		file_types[file_extension] = 1
	
	return file_types


def count_sort_by_file_type(directory):
	files_list = fileSystemHelper.list_nested_files_in_path(directory)
	
	file_types = file_types_counter(files_list)
	
	sorted_file_types = dict(sorted(file_types.items(), key=lambda item: item[1], reverse=True))
	sorted_file_types_list = list(sorted_file_types.keys())
	return sorted_file_types_list


def analyze_consumer():
	consumer = Consumer('analyze_queue')
	
	def callback(channel, method, properties, body):
		logger.info("Got a message from 'analyze_queue'")
		
		sorted_file_types_list = count_sort_by_file_type(PATH_TO_SEARCH_IN)
		top_10_file_types_in_theharvester = sorted_file_types_list[0:10]
		send_analyze_message(top_10_file_types_in_theharvester)
	
	consumer.subscribe(callback)


if __name__ == '__main__':
	logger.info("Analyze module is listening...")
	MessageBroker.wait_for_connection()
	analyze_consumer()
