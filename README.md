# 📱SKRIPSI - YouTube Live Chat Sentiment Analysis (Real-Time Big Data Pipeline)

A real-time system for ingesting, processing, and analyzing YouTube live chat comments using Big Data technologies. Built with **Apache Kafka**, **Apache Spark Structured Streaming**, **Elasticsearch** and **Kibana**, this system performs sentiment analysis using **VADER** and **TextBlob**, and visualizes results on a live dashboard.

---

## 🔧 Tech Stack
![Image](https://github.com/user-attachments/assets/72cbdd49-ff94-4b62-8c49-65f2d343a95c)

- **Apache Kafka** – Message broker for real-time data ingestion & real-time data streaming
- **Apache Spark Structured Streaming** – Stream processing engine
- **Elasticsearch** – Searchable data store
- **Kibana** – Real-time visualization interface
- **Flask (Python)** – Backend API and WebSocket server
- **React.js** – Frontend dashboard
- **VADER & TextBlob** – Lexicon-based sentiment analysis
- **Docker** – Containerized deployment

---

## 📁 Project Structure

```
.
├── spark/                      # Spark job for sentiment analysis
│   ├── spark_job.py            
│   ├── requirements.txt        
│   └── Dockerfile              
│
├── producer/                   # Kafka producer to collect YouTube live chat
│   ├── producer.py             
│   ├── requirements.txt        
│   └── Dockerfile              
│
├── logs/                       # Log analysis scripts
│
├── sentiment-backend/         # Flask backend for REST API and Socket.IO
│   └── app.py                  
│
├── sentiment-ui/              # React.js frontend for sentiment dashboard
│   ├── src/                    
│   ├── public/                 
│   └── index.html              
│
├── docker-compose.yml         # Multi-container orchestration
├── README.md                  
└── How To Run.txt             # Step-by-step execution guide
```

---

## 📊 Features

- Real-time ingestion of live chat from YouTube via YouTube Data API v3
- Stream processing using Apache Kafka and Spark Structured Streaming
- Lexicon-based sentiment classification using VADER and TextBlob
- Visualization of sentiment distribution on a React-based dashboard
- Additional dashboard analytics via Kibana

![Image](https://github.com/user-attachments/assets/e0d0ca6f-3710-4018-9cc4-d2dae758dbb9)

![Image](https://github.com/user-attachments/assets/97376a82-9684-4f4a-8068-4ae92f6f6f7c)

![Image](https://github.com/user-attachments/assets/76817959-8514-4dca-95b8-7f745d86bd80)
---

## 🧪 Testing and Performance

- System tested on 3 YouTube live streams with 9k, 20k, and 100k viewers
- Kafka Producer: up to **783 messages/min**
- Spark Streaming: up to **14.75 batches/min**
- End-to-end latency: **~9 seconds**
- VADER Accuracy: **93%**
- TextBlob Accuracy: **60%**

---

## 🔮 Future Improvements

- Integrate deep learning models (e.g., BERT, RoBERTa)
- Replace polling with web scraping for live chat collection
- Migrate from Spark to Flink for true continuous stream processing

---

## Notes
- Requires YouTube Data API v3 credentials to collect live chat data
- Set environment variables in `.env` file for API keys and Kafka topic settings

---

## 📝 License

This project is licensed under the MIT License.
