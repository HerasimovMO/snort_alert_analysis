from os import walk
import os
import csv
import re

alert_files = ['test', 'community_alert', 'pulledpork_alert']
file_index = 1


def save(file_name, content_rows):
    with open(f'{file_name}.csv', 'w') as f:
        writer = csv.writer(f)
        for row in content_rows:
            writer.writerow(row)


def read_file(path):
    # get text from file
    with open(f'{path}.txt', 'r') as file:
        return file.read()


def process_log_file(path):
    # read file and split content into an array

    # working directory
    cwd = str(os.getcwd()) + '/stats/'
    file_path = cwd + path

    return read_file(file_path).split('\n\n')


def get_classification_content(debug_str):
    pattern = '(?<=Classification:)(.*)(?=\] \[)'
    matches = re.findall(pattern, debug_str)
    return matches[0].strip() if len(matches) > 0 else 'unknown'


def get_priority(debug_str):
    pattern = '(?<=Priority:) \d'
    matches = re.findall(pattern, debug_str)
    return matches[0].strip() if len(matches) > 0 else 'unknown'


def get_title_content(debug_str):
    pattern = '(?<=\d\])(.*)(?=\[\*\*\])'
    matches = re.findall(pattern, debug_str)
    return matches[0].strip() if len(matches) > 0 else 'unknown'


alert_groups = [['Event', 'Start time',
                 'End time', 'Priority', 'Classification']]

current_event = ''
start_time = ''
end_time = ''
priority = 10
classification = ''

items = process_log_file(alert_files[file_index])
for index, item in enumerate(items):

    log_lines = item.split('\n')
    alert_title = get_title_content(log_lines[0])
    isNew = False

    if len(log_lines) < 3:
        # print(log_lines + ['😂😂😂😂😂😂😂'])
        continue

    time = log_lines[2].split(' ')[0]

    if current_event == '':
        print('created empty values')
        current_event = alert_title
        start_time = time
        end_time = time
        priority = get_priority(log_lines[1])
        classification = get_classification_content(log_lines[1])
        continue

    if alert_title == current_event and index != (len(items) - 1):
        end_time = time
    else:
        alert_groups.append(
            [current_event, start_time, end_time, priority, classification])
        current_event = alert_title
        start_time = time
        end_time = time
        priority = get_priority(log_lines[1])
        classification = get_classification_content(log_lines[1])

filtered_alerts = list(
    filter(lambda x: 'connection attempt' not in x[0], alert_groups))

print(file_index)
save(alert_files[file_index] + '_all_events', alert_groups)
save(alert_files[file_index] + '_warning_events', filtered_alerts)
