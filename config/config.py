import os
from dotenv import load_dotenv

from logger_config import logger

# Load environment variables from .env file
load_dotenv()

# OpenWeather API settings
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
logger.info("Connecting to OpenWeather API using key: %s", OPENWEATHER_API_KEY)

# Kafka settings
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
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
