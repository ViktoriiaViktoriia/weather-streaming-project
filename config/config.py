import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from .logger_config import logger

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
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)    # Create SQLAlchemy engine

# Google Cloud Storage bucket
GCS_BUCKET = os.getenv("GCS_BUCKET")
logger.info("Accessing GCS Bucket: %s", GCS_BUCKET)
STORAGE_MAX_USAGE_GB = float(os.getenv("STORAGE_MAX_USAGE_GB"))

# OpenWeather API Limits
API_CALLS_PER_DAY = 30000

# Selected cities within free API limits
CITIES = ["Helsinki", "Tampere", "Oulu"]
NUM_CITIES = len(CITIES)

RAW_DIR = os.getenv("RAW_DIR", "weather_raw_data")
PROCESSED_DIR = os.getenv("PROCESSED_DIR", os.path.join(RAW_DIR, "processed"))
