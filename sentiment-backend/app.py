from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from elasticsearch import Elasticsearch
import time
import os
import requests
import threading

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load configuration from environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
VIDEO_ID = os.getenv("VIDEO_ID")

# Check Elasticsearch connection
try:
    es = Elasticsearch("http://localhost:9200")
    if not es.ping():
        raise ValueError("Elasticsearch cannot be reached.")
except Exception as e:
    print(f"Error: {e}")
    es = None

@app.route("/")
def home():
    return jsonify({"message": "Backend Flask is running!"})

@app.route("/chat", methods=["GET"])
def get_chat():
    if es is None:
        return jsonify({"error": "Elasticsearch is not available"}), 500

    try:
        response = es.search(index="sentiment-analysis", body={
            "size": 10000,
            "sort": [{"published_at": {"order": "asc"}}],
            "query": {"match_all": {}}
        })

        messages = [
            {
                "author": hit["_source"].get("author", "Unknown"),
                "message": hit["_source"].get("message", ""),
                "final_sentiment": hit["_source"].get("final_sentiment", "neutral"),
                "published_at": hit["_source"].get("published_at", "")
            }
            for hit in response["hits"]["hits"]
        ]
        return jsonify(messages)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/viewers", methods=["GET"])
def get_viewers():
    if not YOUTUBE_API_KEY or not VIDEO_ID:
        return jsonify({"error": "YOUTUBE_API_KEY or VIDEO_ID is not available"}), 500

    url = f"https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id={VIDEO_ID}&key={YOUTUBE_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        viewers = data.get("items", [{}])[0].get("liveStreamingDetails", {}).get("concurrentViewers", 0)
        return jsonify({"count": int(viewers)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/video-info", methods=["GET"])
def get_video_info():
    if not YOUTUBE_API_KEY or not VIDEO_ID:
        return jsonify({"error": "YOUTUBE_API_KEY or VIDEO_ID is not available"}), 500

    video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={VIDEO_ID}&key={YOUTUBE_API_KEY}"
    try:
        video_response = requests.get(video_url).json()
        snippet = video_response.get("items", [{}])[0].get("snippet", {})

        title = snippet.get("title", "Title not found")
        channel_id = snippet.get("channelId", None)

        if not channel_id:
            return jsonify({"error": "Channel ID not found"}), 500

    except Exception as e:
        return jsonify({"error": f"Failed to fetch video data: {str(e)}"}), 500

    channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={YOUTUBE_API_KEY}"
    try:
        channel_response = requests.get(channel_url).json()
        thumbnails = channel_response.get("items", [{}])[0].get("snippet", {}).get("thumbnails", {})

        # Get the best quality image available
        logo_url = (
            thumbnails.get("maxres", {}).get("url") or
            thumbnails.get("high", {}).get("url") or
            thumbnails.get("medium", {}).get("url") or
            thumbnails.get("default", {}).get("url")
        )

        return jsonify({"title": title, "logo_url": logo_url})

    except Exception as e:
        return jsonify({"error": f"Failed to fetch channel logo: {str(e)}"}), 500

def watch_elasticsearch():
    last_timestamp = None
    while True:
        if es is None:
            continue
        try:
            response = es.search(index="sentiment-analysis", body={
                "size": 10,
                "sort": [{"published_at": {"order": "desc"}}],
                "query": {"match_all": {}}
            })

            if response["hits"]["hits"]:
                new_messages = []
                for hit in response["hits"]["hits"]:
                    chat = hit["_source"]
                    timestamp = chat["published_at"]
                    if last_timestamp is None or timestamp > last_timestamp:
                        new_messages.append(chat)

                if new_messages:
                    last_timestamp = new_messages[-1]["published_at"]
                    socketio.emit("new_messages", new_messages)
        except Exception as e:
            print(f"Error watching Elasticsearch: {e}")
        time.sleep(2)

def emit_viewer_count():
    while True:
        if not YOUTUBE_API_KEY or not VIDEO_ID:
            continue
        try:
            response = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id={VIDEO_ID}&key={YOUTUBE_API_KEY}")
            data = response.json()
            viewers = data.get("items", [{}])[0].get("liveStreamingDetails", {}).get("concurrentViewers", 0)
            socketio.emit("viewer_count", int(viewers))
        except Exception as e:
            print(f"Error fetching viewer count: {e}")
        time.sleep(5)

if __name__ == "__main__":
    watch_thread = threading.Thread(target=watch_elasticsearch, daemon=True)
    watch_thread.start()
    viewer_thread = threading.Thread(target=emit_viewer_count, daemon=True)
    viewer_thread.start()
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
