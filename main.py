from config import logger
from ingestion import stream_weather_data


def main():
    try:
        # Start weather data streaming
        stream_weather_data()
        logger.info("Weather data streamed successfully.")
    except KeyboardInterrupt:
        logger.info("Weather data streaming interrupted.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
