import json
import csv
from datetime import datetime
from confluent_kafka import Consumer, KafkaError

from config import (logger, KAFKA_TOPIC, KAFKA_TOPIC_FORECAST, KAFKA_BROKER, GCS_BUCKET)
from storage import upload_to_gcs


def weather_data_consumer():
    # Configuration
    timestamp_str = datetime.now().strftime("%Y%m%d")
    weather_csv_path = f"weather_raw_data/weather_raw_data_{timestamp_str}.csv"

    # Kafka configuration
    kafka_config = {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "weather-consumer-group",
        "auto.offset.reset": "earliest",  # Read from beginning if no committed offset
    }

    # Initialize Kafka consumer
    consumer = Consumer(kafka_config)
    consumer.subscribe([KAFKA_TOPIC, KAFKA_TOPIC_FORECAST])

    logger.info("Kafka consumer is now running.")

    try:
        while True:
            message = consumer.poll(1.0)  # wait max 1 second for a message

            if message is None:
                continue  # no message received yet
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue  # end of partition event
                elif "Connection refused" in str(message.error()):
                    logger.info("[Error] Kafka not available. Exiting loop.")
                    break
                else:
                    logger.info(f"Consumer error: {message.error()}")
                    break
            logger.info(f"Received message from topic: {message.topic()}")

            data = json.loads(message.value().decode("utf-8"))
            # print("RAW KAFKA MESSAGE:", data)
            topic = data.get("type", "unknown")

            # Consume and write to CSV
            with open(weather_csv_path, mode='a', newline='') as file:
                fieldnames = ["type", "city", "description", "temperature", "feels_like", "humidity", "wind",
                              "pressure", "timestamp"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                # Write header only once if file is empty
                if file.tell() == 0:
                    writer.writeheader()

                if topic == KAFKA_TOPIC:
                    writer.writerow({
                        "type": data["type"],
                        "city": data["name"],
                        "description": data["weather"][0]["description"],
                        "temperature": data["main"]["temp"],
                        "feels_like": data["main"]["feels_like"],
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "pressure": data["main"]["pressure"],
                        "timestamp": data["dt"]
                    })
                elif topic == KAFKA_TOPIC_FORECAST:
                    # print("RAW KAFKA MESSAGE:", data)
                    writer.writerow({
                        "type": data["type"],
                        "city": data["city"]["name"],
                        "description": data["list"][0]["weather"][0]["description"],
                        "temperature": data["list"][0]["main"]["temp"],
                        "feels_like": data["list"][0]["main"]["feels_like"],
                        "humidity": data["list"][0]["main"]["humidity"],
                        "wind": data["list"][0]["wind"]["speed"],
                        "pressure": data["list"][0]["main"]["pressure"],
                        "timestamp": data["list"][0]["dt"]
                    })
                # Upload to GCS
                upload_to_gcs(weather_csv_path, GCS_BUCKET, f"raw_weather_data/{weather_csv_path}")

    except KeyboardInterrupt:
        logger.info("\n[Shutdown] Interrupted by user.")
    except Exception as e:
        logger.error(f"Kafka consumer crashed: {e}")
    finally:
        consumer.close()
        logger.info("[Shutdown] Kafka consumer closed.")






