import json
import requests
from confluent_kafka import Producer
import schedule
import time

from config import logger, API_KEY, BASE_URL, KAFKA_TOPIC, KAFKA_TOPIC_FORECAST, KAFKA_BROKER


# OpenWeather API Limits
API_CALLS_PER_DAY = 30000
# Selected cities within free API limits
CITIES = ["Helsinki", "Tampere", "Oulu"]
NUM_CITIES = len(CITIES)

# Calculate the interval
REQUESTS_PER_CITY = API_CALLS_PER_DAY // NUM_CITIES  # Max requests per city per day
INTERVAL_SECONDS = 10  # Time between API calls per city
logger.info(f"Fetching weather data every {INTERVAL_SECONDS // 60} minutes per city.")

# Kafka configuration
KAFKA_CONFIG = {
    "bootstrap.servers": KAFKA_BROKER,
}

# Create a Kafka producer
producer = Producer(KAFKA_CONFIG)


# Fetch weather data from OpenWeather API
def fetch_weather(url, city):
    """Fetches weather data while staying within API limits."""

    try:
        response = requests.get(url)
        response.raise_for_status()     # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()        # If request is successful, return the JSON data

    except requests.exceptions.HTTPError as http_err:
        logger.info(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.info(f"Request error occurred for {city}: {req_err}")
    logger.error(f"Error fetching data for {city}")
    return None  # Return None if any exception occurs


def send_message_to_kafka(topic, data):
    """Sends weather data to Kafka topic."""
    try:
        producer.produce(topic, key=None, value=json.dumps(data).encode("utf-8"))
        producer.flush()  # Ensure the message is sent
        logger.info(f"Data sent to Kafka topic {topic}")
    except Exception as e:
        logger.info(f"Error sending message to Kafka: {e}")


def stream_weather_data():
    """Periodically fetches weather data with automatic retries and exponential backoff,
    then streams it to Kafka."""

    for city in CITIES:
        retries = 0      # Reset retry counter for each city
        max_retries = 5

        while retries < max_retries:  # Retry logic applies to the current city
            try:
                url = f"{BASE_URL}/weather?q={city}&APPID={API_KEY}"
                weather_data = fetch_weather(url, city)
                logger.info(f"Successfully fetched data for {city}")

                if weather_data:
                    send_message_to_kafka(KAFKA_TOPIC, weather_data)
                    logger.info(f"Sent weather data for {city} to Kafka.")
                break  # Exit retry loop for the current city if successful

            except Exception as e:
                logger.warning(f"Failed to fetch data for {city}: {e}. Retrying...")
                retries += 1

                if retries < max_retries:
                    logger.info(f"Retrying in {INTERVAL_SECONDS / 60:.2f} minutes...")
                    time.sleep(INTERVAL_SECONDS)
                else:
                    logger.error(f"Max retries reached for {city}. Skipping.")
                    break  # Exit retry loop if max retries are reached


def fetch_forecast():
    """Fetches forecast weather data."""

    for city in CITIES:
        try:
            url = f"{BASE_URL}/forecast?q={city}&APPID={API_KEY}"

            forecast_data = fetch_weather(url, city)
            logger.info(f"Fetched forecast for {city}")

            if forecast_data:
                logger.info(f"Successfully fetched forecast data for {city}.")
                send_message_to_kafka(KAFKA_TOPIC_FORECAST, forecast_data)
                logger.info(f"Forecast data sent for {city} to Kafka.")
            else:
                logger.warning(f"No forecast data retrieved for {city}.")

        except Exception as e:
            logger.error(f"Failed to fetch forecast for {city}: {e}")


def schedule_forecast():
    """Schedules periodic fetching of 5-day forecasts for selected cities."""

    schedule.every(12).hours.do(fetch_forecast)
    logger.info("Forecast scheduler initialized.")

    try:
        while True:
            schedule.run_pending()
            logger.info("Waiting for the next scheduled forecast fetch...")
            time.sleep(3600)  # Check for scheduled tasks every hour

    except KeyboardInterrupt:
        logger.info("Stopping scheduled weather data fetch.")
