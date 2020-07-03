from os import walk
import os

alert_files = ['test', 'community_alert', 'pulledpork_alert.txt']


def read_file(path):
    # get text from file
    with open(f'{path}.txt', 'r') as file:
        return file.read()


def process_log_file(path):
    # read file and split content into an array

    # working directory
    cwd = str(os.getcwd()) + '/stats/'
    file_path = cwd + path

    return read_file(file_path).split('\n\n')[:3]


# for item in log_items:
