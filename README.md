# 📱 YouTube Live Chat Sentiment Analysis (Near Real-Time Data Streaming Pipeline)

A near real-time system for ingesting, processing, and analyzing YouTube Live Chat messages using modern Big Data technologies. Built with **Apache Kafka**, **Spark Structured Streaming**, **Elasticsearch**, **Kibana**, **React.js**, and **Flask**, the pipeline performs sentiment analysis using **VADER** and **TextBlob**, and displays the results through an interactive real-time dashboard.

> ⚠️ **Why Near Real-Time?**
> The system operates in **near real-time** due to two key constraints:
> 1. **YouTube Data API Rate Limit** – The API enforces a **minimum 4–5 second polling interval** and does not support continuous streaming, which limits the granularity of live chat data ingestion.
> 2. **Micro-Batch Processing with Spark Structured Streaming** – Spark processes data in small intervals (e.g., every 2–5 seconds), introducing slight latency between data ingestion and analysis.

---

## 🔧 Tech Stack

![Data Pipeline2](https://github.com/user-attachments/assets/384d4341-ddf0-4a7a-bdf2-6448aa926a3d)
The pipeline consists of five key stages:
① **YouTube Live Chat** messages are retrieved using the YouTube Data API v3 by a Kafka producer.
② Messages are sent to **Apache Kafka**, which serves as the message broker.
③ **Apache Spark Structured Streaming** consumes the data, performs cleaning, transformation, and sentiment analysis (VADER & TextBlob).
④ The processed data is stored and indexed in **Elasticsearch**.
⑤ Results are visualized through **Kibana** and a custom **React.js + Flask** dashboard using WebSockets.

### Tools Used:
* **[YouTube Data API v3](https://developers.google.com/youtube/v3)** – Data source for live chat messages
* **[Apache Kafka](https://kafka.apache.org/)** – Distributed message broker for real-time ingestion
* **[Apache Spark Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)** – Stream processing engine
* **[VADER](https://github.com/cjhutto/vaderSentiment)** & **[TextBlob](https://textblob.readthedocs.io/)** – Lexicon-based sentiment analysis tools
* **[Elasticsearch](https://www.elastic.co/elasticsearch/)** – Searchable data store
* **[Kibana](https://www.elastic.co/kibana/)** – Visualization and analytics tool for Elasticsearch
* **[Flask](https://flask.palletsprojects.com/)** – Lightweight backend API and WebSocket server
* **[Socket.IO](https://socket.io/)** – Real-time communication between backend and frontend
* **[React.js](https://reactjs.org/)** – Frontend framework for real-time UI
* **[Recharts](https://recharts.org/)** – Charting library for visualizing sentiment trends
* **[Docker](https://www.docker.com/)** – Containerized deployment with orchestration via Docker Compose

---

## 🚀 Getting Started

### Prerequisites

* Docker & Docker Compose installed
* YouTube Data API v3 key

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. Set up `.env` file with your credentials:

```env
YOUTUBE_API_KEY=your_api_key
VIDEO_ID=your_video_id
KAFKA_TOPIC=your_topic
```

---

## 📁 Project Structure

```
.
├── docker-compose.yml             # Docker orchestration
├── .env                           # API keys and configs
│
├── logs/                          # Log files
│
├── producer/                      # Kafka producer for YouTube live chat
│   ├── Dockerfile
│   ├── producer.py
│   └── requirements.txt
│
├── spark/                         # Spark job for sentiment analysis
│   ├── Dockerfile
│   ├── spark_job.py
│   ├── requirements.txt
│   └── speed_test.txt             # Performance testing log
│
├── sentiment-backend/            # Flask backend (REST API + Socket.IO)
│   └── app.py
│
├── sentiment-ui/                 # React frontend
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── img/                           # Visual assets
├── README.md                      # Main documentation
├── How To Run (Eng).txt           # English guide
└── How To Run (Idn).txt           # Indonesian guide
```

---

## 📌 Usage Flow

1. Kafka producer collects live chat messages via YouTube API
2. Messages are streamed to Kafka topics
3. Spark consumes messages and applies sentiment analysis
4. Processed data is sent to Elasticsearch
5. React dashboard displays data in near real-time via Socket.IO
6. Kibana provides advanced historical analysis and search capabilities

---

## 📊 Features

* ⏱️ Near real-time ingestion of YouTube live chat
* 🔄 Stream processing via Kafka and Spark
* 💬 Sentiment analysis using VADER & TextBlob
* 📈 Live sentiment dashboard (React + Socket.IO)
* 📊 Historical analytics and search with Kibana

![web](https://github.com/user-attachments/assets/d3216a0b-ca47-41ec-a1fe-d4fc794a9c1d)
![web2](https://github.com/user-attachments/assets/f4719a60-070e-464e-a117-ef849e745a9e)
![kibana](https://github.com/user-attachments/assets/ef5f806c-dbdb-4055-bc06-ece18abc0ec3)
![kibana2](https://github.com/user-attachments/assets/589417bc-3022-41f9-aee2-49058c7ec48f)

---

## 🧪 Testing & Performance

The system has been benchmarked on high-traffic YouTube live streams:

| Metric                      | Result                      |
| --------------------------- | --------------------------- |
| Viewer Count (tested)       | 9K, 20K, 100K               |
| Kafka Producer Throughput   | Up to **783 messages/min**  |
| Spark Processing Rate       | Up to **14.75 batches/min** |
| End-to-End Latency          | \~**9 seconds**             |
| VADER Sentiment Accuracy    | **93%**                     |
| TextBlob Sentiment Accuracy | **60%**                     |

---

## 🔮 Future Improvements

* 🧠 Integrate deep learning models (e.g., BERT, RoBERTa)
* 🔍 Explore WebSocket or scraping to bypass API polling
* ⚙️ Migrate to Apache Flink for lower-latency stream processing

---

## ⚠️ Notes

* Requires a valid **YouTube Data API v3** key
* All credentials configured via `.env` file

---

## 📝 License

![License](https://img.shields.io/badge/license-Private_Use_Only-red.svg)

This project is licensed under a **Custom Private License**:

* For **personal, non-commercial use only**
* Redistribution, sublicensing, or commercial use is **prohibited**

© 2025 Andrew Suadnya
