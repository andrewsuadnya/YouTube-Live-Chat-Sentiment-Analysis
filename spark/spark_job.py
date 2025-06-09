import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace, split, from_json, when, pandas_udf, array_join
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.ml.feature import StopWordsRemover
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import pytz

# Konfigurasi logging
log_handler = RotatingFileHandler("logs/spark.log", maxBytes=5*1024*1024, backupCount=5)
logging.basicConfig(level=logging.INFO, handlers=[log_handler, logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "youtube_live_chat")
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")

# Inisialisasi SparkSession
spark = SparkSession.builder \
    .appName("YouTubeLiveChatSentimentAnalysis") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.elasticsearch:elasticsearch-hadoop:8.11.0") \
    .config("spark.executor.memory", "6g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "5") \
    .config("spark.streaming.backpressure.enabled", "true") \
    .config("spark.streaming.kafka.maxRatePerPartition", "200") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Skema data dari Kafka
schema = StructType([
    StructField("author", StringType(), True),
    StructField("message", StringType(), True),
    StructField("published_at", StringType(), True)
])

# Caching Sentiment Analyzer
vader_analyzer = SentimentIntensityAnalyzer()

@pandas_udf(StringType())
def analyze_sentiment_vader(messages: pd.Series) -> pd.Series:
    return messages.apply(lambda msg: (
        "positive" if vader_analyzer.polarity_scores(msg)['compound'] >= 0.05 else
        "negative" if vader_analyzer.polarity_scores(msg)['compound'] <= -0.05 else
        "neutral"
    ))

@pandas_udf(StringType())
def analyze_sentiment_textblob(messages: pd.Series) -> pd.Series:
    return messages.apply(lambda msg: (
        "positive" if TextBlob(msg).sentiment.polarity > 0 else
        "negative" if TextBlob(msg).sentiment.polarity < 0 else
        "neutral"
    ))

# Baca data dari Kafka dengan pembatasan rate
raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .load()

# Parsing JSON dari Kafka
parsed_stream = raw_stream.selectExpr("CAST(value AS STRING) as json_string") \
    .select(from_json(col("json_string"), schema).alias("data")) \
    .select("data.*") \
    .dropDuplicates(["message"])  # Hapus duplikat lebih awal

# Membersihkan teks untuk VADER (hapus URL, mention, angka, karakter non-alfabet, mempertahankan emotikon)
processed_stream = parsed_stream.withColumn(
    "cleaned_message_vader",
    lower(regexp_replace(col("message"), r"https?://\S+|www\.\S+|@\w+|[^a-zA-Z\u1F300-\u1F6FF\u1F900-\u1F9FF\uD83C-\uDBFF\uDC00-\uDFFF\s]|[0-9!@#$%^&*()_+={}\[\]:;\"'<>,.?/~`\\|-]", ""))
)

# Membersihkan teks untuk TextBlob (hapus URL, mention, angka, karakter non-alfabet, emotikon)
processed_stream = processed_stream.withColumn(
    "cleaned_message_textblob",
    lower(regexp_replace(col("message"), r"https?://\S+|www\.\S+|@\w+|[^\w\s]|\d+", ""))
)

# Analisis Sentimen dengan VADER (langsung dari cleaned_message_vader)
processed_stream = processed_stream.withColumn("vader_sentiment", analyze_sentiment_vader(col("cleaned_message_vader")))

# Tokenisasi teks untuk TextBlob
processed_stream = processed_stream.withColumn("tokenized_message", split(col("cleaned_message_textblob"), r"\s+"))

# Menghapus stopwords untuk TextBlob
stopwords_remover = StopWordsRemover(inputCol="tokenized_message", outputCol="filtered_message")
processed_stream = stopwords_remover.transform(processed_stream)

# Gabungkan kembali hasil filtering untuk TextBlob
processed_stream = processed_stream.withColumn("final_message_textblob", array_join(col("filtered_message"), " "))

# Analisis Sentimen dengan TextBlob
processed_stream = processed_stream.withColumn("textblob_sentiment", analyze_sentiment_textblob(col("final_message_textblob")))

# Mencocokkan hasil sentimen
processed_stream = processed_stream.withColumn(
    "sentiment_match",
    when(col("vader_sentiment") == col("textblob_sentiment"), "True").otherwise("False")
)

# Final sentiment berdasarkan Aturan Prioritas
processed_stream = processed_stream.withColumn(
    "final_sentiment",
    when((col("vader_sentiment") == "negative") | (col("textblob_sentiment") == "negative"), "negative")
    .when((col("vader_sentiment") == "positive") | (col("textblob_sentiment") == "positive"), "positive")
    .otherwise("neutral")
)

# Simpan hasil ke Elasticsearch dalam Mode Batch
def write_to_elasticsearch(batch_df, batch_id):
    batch_df.write \
        .format("org.elasticsearch.spark.sql") \
        .option("es.nodes", ELASTICSEARCH_HOST) \
        .option("es.resource", "sentiment-analysis/_doc") \
        .mode("append") \
        .save()

    # Pilih hanya kolom yang ingin dicetak di log
    selected_df = batch_df.select("message", "vader_sentiment", "textblob_sentiment", "sentiment_match", "final_sentiment")
    table_log = selected_df._jdf.showString(20, 0, False)

    # Konversi timestamp ke Asia/Makassar sebelum logging
    local_tz = pytz.timezone("Asia/Makassar")
    utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
    local_time = utc_time.astimezone(local_tz)

    log_message = f"{local_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n{table_log}"
    logger.info(log_message)

output_query = processed_stream.writeStream \
    .foreachBatch(write_to_elasticsearch) \
    .outputMode("append") \
    .option("checkpointLocation", "logs/spark-checkpoints/") \
    .start()

output_query.awaitTermination()
