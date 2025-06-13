import os
import json
import logging
import pytz
import time
from datetime import datetime
from kafka import KafkaProducer
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
VIDEO_ID = os.getenv("VIDEO_ID")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "youtube_live_chat")

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Set timezone to local timezone
local_tz = pytz.timezone('Asia/Makassar')

class LocalTimeFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, local_tz)
        return dt.strftime(datefmt) if datefmt else dt.strftime("%Y-%m-%d %H:%M:%S")

# Configure logging
formatter = LocalTimeFormatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("logs/producer.log")
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler, logging.StreamHandler()])

def convert_to_local_time(utc_time_str):
    """Convert UTC timestamp to local time in ISO 8601 format for Elasticsearch."""
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    return utc_time.astimezone(local_tz).isoformat()

def validate_message(data):
    """Validate the structure and content of a message before sending to Kafka."""
    required_keys = ['author', 'message', 'published_at']
    if not isinstance(data, dict):
        logging.error(f"Invalid message format. Expected dict, got {type(data)}: {data}")
        return False
    for key in required_keys:
        if key not in data or not data[key].strip():
            logging.error(f"Missing or empty key '{key}' in message: {data}")
            return False
    return True

def get_live_chat_id(youtube, video_id):
    """Get live chat ID from a YouTube video ID."""
    try:
        logging.info(f"Fetching live chat ID for video ID: {video_id}")
        response = youtube.videos().list(part="liveStreamingDetails", id=video_id).execute()
        items = response.get('items', [])
        if not items:
            logging.error(f"No items found in API response for video ID: {video_id}")
            return None
        live_chat_id = items[0].get('liveStreamingDetails', {}).get('activeLiveChatId')
        logging.info(f"Live chat ID obtained: {live_chat_id}")
        return live_chat_id
    except (IndexError, KeyError, HttpError) as e:
        logging.error(f"Failed to get live chat ID: {e}")
        return None

def fetch_live_chat_messages(youtube, live_chat_id, producer, max_messages=5000, max_duration=3600):
    """Fetch live chat messages and send them to Kafka."""
    next_page_token = None
    message_count = 0
    start_time = time.time()

    while message_count < max_messages and (time.time() - start_time) < max_duration:
        try:
            response = youtube.liveChatMessages().list(
                liveChatId=live_chat_id,
                part="snippet,authorDetails",
                pageToken=next_page_token
            ).execute()

            messages = response.get('items', [])
            next_page_token = response.get('nextPageToken')

            for message in messages:
                if 'textMessageDetails' in message['snippet']:
                    data = {
                        'author': message['authorDetails']['displayName'],
                        'message': message['snippet']['textMessageDetails']['messageText'],
                        'published_at': convert_to_local_time(message['snippet']['publishedAt'])
                    }

                    if validate_message(data):
                        try:
                            producer.send(KAFKA_TOPIC, value=data)
                            logging.info(f"Sent to Kafka: {data}")
                            message_count += 1
                        except Exception as e:
                            logging.error(f"Failed to send message to Kafka: {e}")
                    else:
                        logging.warning(f"Invalid data skipped: {data}")
                else:
                    logging.warning(f"Message skipped due to missing 'textMessageDetails': {message}")

            # Add delay to comply with API rate limits
            time.sleep(5)  # Adjust based on API response rate
        except HttpError as e:
            if e.resp.status == 403 and "rateLimitExceeded" in str(e):
                logging.error(f"Rate limit exceeded. Waiting for 10 seconds before retrying.")
                time.sleep(10)
            else:
                logging.error(f"Failed to fetch live chat messages: {e}")
                break

    logging.info(f"Stopped fetching after {message_count} messages or {(time.time() - start_time):.2f} seconds.")

if __name__ == "__main__":
    try:
        logging.info("Starting Kafka producer...")
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all'  # Wait for confirmation from Kafka before considering the message sent
        )
        logging.info("Kafka producer connected successfully.")

        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        live_chat_id = get_live_chat_id(youtube, VIDEO_ID)

        if live_chat_id:
            logging.info(f"Fetching live chat messages for chat ID: {live_chat_id}")
            fetch_live_chat_messages(youtube, live_chat_id, producer, max_messages=5000, max_duration=3600)
        else:
            logging.error("No live chat ID found. Exiting.")
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")
    finally:
        if 'producer' in locals() and producer is not None:
            logging.info("Closing the Kafka producer with 5 seconds timeout.")
            producer.close(timeout=5)
