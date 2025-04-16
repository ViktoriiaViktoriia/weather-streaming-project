import threading
from threading import Thread
import time

from config import logger, API_KEY, BASE_URL, CITIES
from ingestion import stream_weather_data, schedule_forecast
from processing import weather_data_consumer


def main():

    try:
        # Start the consumer in a background thread
        consumer_thread = threading.Thread(target=weather_data_consumer, daemon=True)
        consumer_thread.start()
        logger.info("Kafka consumer started.")

        forecast_threads = []

        while True:
            for city in CITIES:
                # Start current weather data streaming
                stream_weather_data(f"{BASE_URL}/weather?q={city}&APPID={API_KEY}", city)

                # Schedule forecast (only once per city)
                if not any(city in thread.name for thread in forecast_threads):
                    try:
                        url = f"{BASE_URL}/forecast?q={city}&APPID={API_KEY}"
                        thread = threading.Thread(
                            target=schedule_forecast,
                            args=(url, city),
                            name=f"forecast-{city}",
                            daemon=True
                        )
                        thread.start()
                        forecast_threads.append(thread)
                        logger.info(f"Forecast updates are scheduled for {city}.")
                    except Exception as e:
                        logger.error(f"Error starting forecast thread for {city}: {e}")

            # Sleep before next round of current weather fetching
            time.sleep(1 * 60)

    except KeyboardInterrupt:
        logger.info("Weather data streaming interrupted.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}. Failed to process data.")
    finally:
        logger.info("Main thread exiting.")


if __name__ == "__main__":
    main()
