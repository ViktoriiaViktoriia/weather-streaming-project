import json
import requests
from confluent_kafka import Producer
import time

from config import logger, API_KEY, BASE_URL, KAFKA_TOPIC, KAFKA_BROKER


# Selected cities within free API limits
CITIES = ["Helsinki", "Tampere", "Oulu"]

# Kafka configuration
KAFKA_CONFIG = {
    "bootstrap.servers": KAFKA_BROKER,
}

# Create a Kafka producer
producer = Producer(KAFKA_CONFIG)


# Fetch weather data from OpenWeather API
def fetch_weather(city):
    """Fetches weather data while staying within API limits."""
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

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
        backoff_time = 300   # Initial backoff time in seconds (5 minutes)

        while retries < max_retries:  # Retry logic applies to the current city
            try:
                weather_data = fetch_weather(city)
                logger.info(f"Successfully fetched data for {city}")

                if weather_data:
                    send_message_to_kafka(KAFKA_TOPIC, weather_data)
                    logger.info(f"Sent weather data for {city} to Kafka.")
                break  # Exit retry loop for the current city if successful

            except Exception as e:
                logger.warning(f"Failed to fetch data for {city}: {e}. Retrying...")
                retries += 1

                if retries < max_retries:
                    logger.info(f"Retrying in {backoff_time / 60:.2f} minutes...")
                    time.sleep(backoff_time)
                    backoff_time *= 2  # Doubles backoff time for the current city
                else:
                    logger.error(f"Max retries reached for {city}. Skipping.")





