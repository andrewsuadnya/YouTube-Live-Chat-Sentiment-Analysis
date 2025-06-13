# 📱 YouTube Live Chat Sentiment Analysis (Near Real-Time Data Pipeline)

A near real-time system for ingesting, processing, and analyzing YouTube Live Chat comments using modern Big Data technologies. Built using **Apache Kafka**, **Spark Structured Streaming**, **Elasticsearch**, **Kibana**, **React.js**, and **Flask**, this pipeline performs sentiment analysis using **VADER** and **TextBlob**, and visualizes results on an interactive dashboard.

> ⚠️ **Why Near Real-Time?**  
> The system is categorized as **near real-time** due to two key constraints:  
> 1. **YouTube Data API Rate Limits** – The API enforces a **minimum 4-5 second polling interval** and does not support continuous real-time streaming, which limits the granularity of live chat data collection.  
> 2. **Micro-Batch Processing in Spark Structured Streaming** – Spark processes data in small batches (e.g., every 2–5 seconds), not per individual message, resulting in slight latency between ingestion and analysis.

---

## 🔧 Tech Stack

![Data Pipeline2](https://github.com/user-attachments/assets/384d4341-ddf0-4a7a-bdf2-6448aa926a3d)
The data pipeline consists of five main stages:
① YouTube Live Chat is retrieved using the YouTube Data API v3 by a custom Kafka producer.
② The messages are ingested into Apache Kafka, acting as a distributed messaging system.
③ Apache Spark Structured Streaming consumes data from Kafka, performs cleaning, transformation, and sentiment analysis (VADER & TextBlob).
④ The enriched data is sent to Elasticsearch for storage and indexing.
⑤ Data is then visualized in near real-time via Kibana and a custom React.js + Flask dashboard using WebSockets.

* **[YouTube Data API v3](https://developers.google.com/youtube/v3)** – Retrieves live chat messages from YouTube (data source)
* **[Apache Kafka](https://kafka.apache.org/)** – Message broker for real-time data ingestion
* **[Apache Spark Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)** – Stream processing engine for data cleaning, transformation, and sentiment analysis
* **[VADER](https://github.com/cjhutto/vaderSentiment)** & **[TextBlob](https://textblob.readthedocs.io/)** – Lexicon-based sentiment analysis
* **[Elasticsearch](https://www.elastic.co/elasticsearch/)** – Searchable data store for storing analyzed data
* **[Kibana](https://www.elastic.co/kibana/)** – Real-time analytics visualization tool for querying Elasticsearch
* **[Flask](https://flask.palletsprojects.com/)** – Lightweight backend API and WebSocket server
* **[Socket.IO](https://socket.io/)** – Real-time communication between backend and frontend
* **[React.js](https://reactjs.org/)** – Frontend framework for real-time sentiment dashboard
* **[Recharts](https://recharts.org/)** – Charting library used in the React dashboard for visualizing sentiment trends
* **[Docker](https://www.docker.com/)** – Containerized deployment with multi-service orchestration

---

## 🚀 Getting Started

### Prerequisites

* Docker & Docker Compose
* YouTube Data API v3 key

### Installation

1. Clone this repository:

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
├── docker-compose.yml               # Multi-container orchestration
├── .env                             # Environment configuration
│
├── logs/                            # Log analysis scripts or logs
│
├── producer/                       # Kafka producer to collect YouTube live chat
│   ├── Dockerfile
│   ├── producer.py
│   └── requirements.txt
│
├── spark/                           # Spark job for sentiment analysis
│   ├── Dockerfile                   
│   ├── spark_job.py                 
│   ├── requirements.txt            
│   └── speed_test.txt              # Performance testing log
│
├── sentiment-backend/              # Flask backend (REST API & Socket.IO)
│   └── app.py
│
├── sentiment-ui/                   # React.js frontend for sentiment dashboard
│   ├── public/
│   ├── src/
│   ├── node_modules/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── eslint.config.js
│   ├── .gitignore
│   └── README.md
│
├── img/                             # image assets
│
├── README.md                        # Main documentation
├── How To Run (Eng).txt             # Step-by-step guide (English)
└── How To Run (Idn).txt             # Step-by-step guide (Bahasa Indonesia)
```

---

## 📌 Usage

1. Kafka producer collects YouTube Live Chat using the Data API v3.
2. Chat messages are streamed to Kafka topics in real-time.
3. Spark Structured Streaming processes messages and performs sentiment analysis.
4. Results are indexed into Elasticsearch.
5. React + Socket.IO dashboard visualizes data in near real-time.
6. Kibana dashboard allows for deeper historical analysis.

---

## 📊 Features

* ⏱️ Near real-time ingestion of YouTube Live Chat messages
* 🔄 Stream processing using Kafka & Spark Structured Streaming
* 💬 Sentiment classification via VADER and TextBlob
* 📈 Live dashboard using React + Socket.IO
* 📊 Historical and advanced analytics via Kibana

![web](https://github.com/user-attachments/assets/07315439-d078-42d7-8e1c-8bd2223742e0)
![Image](https://github.com/user-attachments/assets/a44c717f-5ffc-4f4f-a730-068bee485466)
![Image](https://github.com/user-attachments/assets/e0d0ca6f-3710-4018-9cc4-d2dae758dbb9)
![kibana](https://github.com/user-attachments/assets/45075e59-c8c8-4d1f-b1db-c4159a8594d8)

---

## 🧪 Testing and Performance

The system has been tested with high-traffic YouTube live streams:

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
* 🔍 Replace API polling with WebSocket or scraping approach
* ⚙️ Migrate from Spark to Flink for lower-latency streaming

---

## ⚠️ Important Notes

* Requires valid **YouTube Data API v3** key
* Configuration via `.env` file (API key, video ID, Kafka topic, etc.)

---

## 📝 License

![License](https://img.shields.io/badge/license-Private_Use_Only-red.svg)

This project is licensed under a **Custom Private License**:

* For **personal, non-commercial use only**.
* Redistribution, sublicensing, or commercial usage is **not permitted**.

Copyright © 2025 Andrew Suadnya
