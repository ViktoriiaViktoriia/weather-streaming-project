import os
import threading
from threading import Thread
import time

from config import logger, API_KEY, BASE_URL, CITIES, RAW_DIR, PROCESSED_DIR
from ingestion import stream_weather_data, schedule_forecast
from processing import weather_data_consumer, load_all_csvs


def main():

    try:
        os.makedirs(PROCESSED_DIR, exist_ok=True)

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

            logger.info(" Starting weather data processing...")
            result_df = load_all_csvs(RAW_DIR, PROCESSED_DIR)

            if not result_df.empty:
                logger.info(" ELT pipeline finished with data inserted.")
            else:
                logger.info(" No new data was found.")

            # Sleep before next round of current weather fetching
            time.sleep(5 * 60)

    except KeyboardInterrupt:
        logger.info("Weather data streaming interrupted.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}. Failed to process data.")
    finally:
        logger.info("Main thread exiting.")


if __name__ == "__main__":
    main()
