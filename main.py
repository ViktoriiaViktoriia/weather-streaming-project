from config import logger, API_KEY, BASE_URL, CITIES
from ingestion import stream_weather_data, schedule_forecast


def main():
    try:
        for city in CITIES:
            # Start weather data streaming
            stream_weather_data(f"{BASE_URL}/weather?q={city}&APPID={API_KEY}", city)

            # Handles scheduled forecast fetching
            schedule_forecast(f"{BASE_URL}/forecast?q={city}&APPID={API_KEY}", city)
    except KeyboardInterrupt:
        logger.info("Weather data streaming interrupted.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
