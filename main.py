import time

from config import logger
from ingestion import stream_weather_data


def main():
    try:
        # Main loop to periodically fetch and stream weather data
        while True:
            # Handles the periodic fetching and sending of weather data
            stream_weather_data()
            logger.info(f"Weather data for streamed successfully.")

            # Sleep for 5 minutes (300 seconds) before the next fetch
            logger.info(f"Waiting for 5 minutes before fetching data again...")
            time.sleep(300)
    except KeyboardInterrupt:
        logger.info("Weather data streaming interrupted.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
