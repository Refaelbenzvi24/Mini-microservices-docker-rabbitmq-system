import os
import json


def get_full_path(relative_path):
	absolute_path = os.path.dirname(__file__)
	full_path = os.path.join(absolute_path, relative_path)
	return full_path


def list_nested_files_in_path(path: str) -> [str]:
	"""
		Loop through a given path and returns all nested files in it.
	"""
	files_list = []
	
	def list_files_in_path(path):
		directory = get_full_path(path)
		for file in os.listdir(directory):
			file_name, file_extension = os.path.splitext(file)
			file_path = get_full_path(f'{directory}/{file_name}{file_extension}')
			
			if os.path.isdir(file_path):
				list_files_in_path(file_path)
			
			if os.path.isdir(file_path) is False:
				files_list.append({'file': file, 'directory': directory})
	
	list_files_in_path(path)
	
	return files_list


def read_json_file(filePath):
	file = open(filePath, "r", encoding='utf-8')
	data = file.read()
	data = json.loads(data)
	return data


def write_to_json_file(data, filePath):
	with open(filePath, "w+", encoding='utf-8') as file:
		json.dump(data, file, skipkeys=False, ensure_ascii=False)
