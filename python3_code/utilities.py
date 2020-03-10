#!/bin/python3

import csv
import datetime
import time

from python3_code.global_vars import delimiter

csv.register_dialect("pipes", delimiter="|")


def convert_millis_to_human(timestamp):
    # e.g. of format in which it'll return -> 2019-11-26 17:13:32.808000
    return datetime.datetime.fromtimestamp(float(timestamp) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')


def get_current_time_millis():
    # fetch current timestamp based on system's epoch footprint
    return int(round(time.time() * 1000))


def current_human_time():
    # Return value of current system time in human readable format
    return convert_millis_to_human(get_current_time_millis())


def get_trimmed_content_from_file(file_path):
    with open(file_path, 'r') as file:
        trimmed_file_content = []
        for current_line in file.readlines():
            trimmed_elements_line = delimiter.join(element.strip() for element in current_line.split(delimiter))
            if trimmed_elements_line not in ['', delimiter, delimiter + delimiter]:
                trimmed_file_content = trimmed_file_content + [trimmed_elements_line]
    return trimmed_file_content


# This will truncate the file and replace it with whatever content is sent in args
# Will help in housekeeping the file at regular intervals to get rid of false writes/newlines introduced, etc
def overwrite_file(file_path, file_content):
    with open(file_path, 'w', newline='\n', encoding='utf-8') as file_object:
        file_object.write(file_content)


def append_to_file(file_path, data_value):
    # Following the structure of both of our CSV files right now -> "DATA|TIME(millis)|TIME(human)"
    # This utility makes it easier for us to format at just this one place if the CSV structure changes
    with open(file_path, 'a', newline='\n', encoding='utf-8') as update_file:
        csv_writer = csv.writer(update_file, dialect="pipes")
        csv_writer.writerow((data_value, get_current_time_millis(), current_human_time()))
