import os
from dotenv import load_dotenv

from logger_config import logger

# Load environment variables from .env file
load_dotenv()

# OpenWeather API settings
BASE_URL = os.getenv("OPENWEATHER_BASE_URL")
API_KEY = os.getenv("OPENWEATHER_API_KEY")
logger.info("Connecting to OpenWeather API using key: %s", API_KEY)

# Kafka settings
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_TOPIC_FORECAST = os.getenv("KAFKA_TOPIC_FORECAST")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
logger.info("Connecting to Kafka broker at %s on topic %s", KAFKA_BROKER, KAFKA_TOPIC)

# Fetch PostgreSQL settings
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
logger.info("Connecting to PostgreSQL database %s on %s:%s", DB_NAME, DB_HOST, DB_PORT)

# Google Cloud Storage bucket
GCS_BUCKET = os.getenv("GCS_BUCKET")
logger.info("Accessing GCS Bucket: %s", GCS_BUCKET)

# GCP Quota Limits (Free Tier)
# BQ_MAX_USAGE_GB = 1000  # 1TB BigQuery free-tier limit
# PUBSUB_MAX_USAGE_GB = 10  # 10GB free-tier limit
# STORAGE_MAX_USAGE_GB = 5  # 5GB free-tier limit