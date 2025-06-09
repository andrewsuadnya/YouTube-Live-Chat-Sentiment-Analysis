import csv
import json
from kafka import KafkaProducer
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Konfigurasi Kafka
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "youtube_live_chat")

# Membuat Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialisasi data ke JSON
)

# File CSV
csv_file = "./input data.csv"

# Membaca file CSV dan mengirim data ke Kafka
with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Membuat pesan dalam format JSON
        kafka_message = {
            "author": "Unknown",  # Anda bisa mengganti ini jika ada kolom author
            "message": row['message'],  # Ambil kolom 'message' dari CSV
            "published_at": datetime.now().isoformat()  # Timestamp saat ini
        }

        # Kirim pesan ke Kafka topic
        producer.send(KAFKA_TOPIC, value=kafka_message)
        print(f"Sent: {kafka_message}")

# Menutup Kafka Producer
producer.close()