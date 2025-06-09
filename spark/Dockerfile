FROM bitnami/spark:latest

# Install Python dan pip
USER root
RUN apt-get update && apt-get install -y python3-pip

# Salin file yang diperlukan
WORKDIR /app
COPY spark_job.py /app/spark_job.py
COPY requirements.txt /app/requirements.txt

# Install dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan Spark job dengan konektor Kafka
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.elasticsearch:elasticsearch-spark-30_2.12:8.11.0", "/app/spark_job.py"]