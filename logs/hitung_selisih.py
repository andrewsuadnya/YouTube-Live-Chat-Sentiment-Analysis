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

# Paling ujung kanan, ganti dengan 'producer' & 'spark' atau 'final_log'
log_folder_producer = 'd:\\Dokumen\\(SKRIPSI)\\..PEMBUATAN SISTEM\\LIVE CHAT SENTIMENT ANALYSIS\\SKRIPSI (SPARK)\\logs\\hitung selisih'
log_folder_spark = 'd:\\Dokumen\\(SKRIPSI)\\..PEMBUATAN SISTEM\\LIVE CHAT SENTIMENT ANALYSIS\\SKRIPSI (SPARK)\\logs\\hitung selisih'

# Ganti dengan 'producer.log' atau 'spark.log'
file_name = 'spark1.log'

file_path = os.path.join(log_folder_spark if file_name == 'spark1.log' else log_folder_producer, file_name)
timestamp_format = "%Y-%m-%d %H:%M:%S.%f" if file_name == 'spark1.log' else "%Y-%m-%d %H:%M:%S"

timestamps = read_log_file(file_path, timestamp_format)
time_differences = calculate_time_differences(timestamps, timestamp_format)

for i, diff in enumerate(time_differences):
    print(f"Selisih waktu antara kelompok pesan {i+1} dan kelompok pesan {i+2}: {diff} detik")

if time_differences:
    average_difference = sum(time_differences) / len(time_differences)
    print(f"Rata-rata selisih waktu: {average_difference:.2f} detik")
else:
    print("Tidak ada selisih waktu yang dapat dihitung.")
