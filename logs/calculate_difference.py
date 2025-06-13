from datetime import datetime
import os

def read_log_file(file_path, timestamp_format):
    timestamps = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if "spark1.log" in file_path and "INFO:__main__:" in line:
                timestamp_str = " ".join(line.split("INFO:__main__:")[1].strip().split()[:2])
            elif "producer3.log" in file_path:
                timestamp_str = " ".join(line.strip().split()[:2])
            else:
                continue
            timestamps.append(timestamp_str)
    return timestamps

def calculate_time_differences(timestamps, timestamp_format):
    datetime_objects = sorted(set(datetime.strptime(ts, timestamp_format) for ts in timestamps))
    return [(datetime_objects[i] - datetime_objects[i-1]).total_seconds() for i in range(1, len(datetime_objects))]

# Use 'logs/producer' and 'logs/spark' folders relative to the project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_folder_producer = os.path.join(BASE_DIR, 'producer')
log_folder_spark = os.path.join(BASE_DIR, 'spark')
# For final logs, you can use:
# log_folder_final = os.path.join(BASE_DIR, 'final_log')

# Change to 'producer.log' or 'spark.log' as needed
file_name = 'producer.log'

file_path = os.path.join(log_folder_spark if file_name == 'spark1.log' else log_folder_producer, file_name)
timestamp_format = "%Y-%m-%d %H:%M:%S.%f" if file_name == 'spark1.log' else "%Y-%m-%d %H:%M:%S"

timestamps = read_log_file(file_path, timestamp_format)
time_differences = calculate_time_differences(timestamps, timestamp_format)

for i, diff in enumerate(time_differences):
    print(f"Time difference between message group {i+1} and message group {i+2}: {diff} seconds")

if time_differences:
    average_difference = sum(time_differences) / len(time_differences)
    print(f"Average time difference: {average_difference:.2f} seconds")
else:
    print("No time differences could be calculated.")