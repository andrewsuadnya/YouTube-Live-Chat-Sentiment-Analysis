FROM bitnami/spark:latest

# Install Python and pip
USER root
RUN apt-get update && apt-get install -y python3-pip

# Copy required files
WORKDIR /app
COPY spark_job.py /app/spark_job.py
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Spark job with Kafka connector
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.elasticsearch:elasticsearch-spark-30_2.12:8.11.0", "/app/spark_job.py"]