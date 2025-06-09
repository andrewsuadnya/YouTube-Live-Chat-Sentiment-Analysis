# Gunakan image Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin semua file ke dalam container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir kafka-python python-dotenv

# Jalankan skrip
CMD ["python", "csv_ke_kafkatopic.py"]