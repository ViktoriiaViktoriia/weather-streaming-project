# 📌 Project: Real-Time Weather Streaming with Kafka & PostgreSQL


## 🚀 Overview
This project fetches weather data from OpenWeather API, streams it using Apache Kafka, and stores it 
in PostgreSQL for analysis.


## 🔹 Features
- Fetches live weather data.
- Streams weather data from OpenWeather API with periodic updates using Kafka.
- Stores processed data in PostgreSQL.
- Allows easy SQL analysis of weather trends.
- Uses CI/CD pipelines for continuous integration, automated testing, and deployment.


## 📦 Tech Stack
- Python (Data ingestion & processing)
- Kafka (Streaming pipeline)
- PostgreSQL (Database storage & analysis)
- Pytest (Unit testing)
- GitHub Actions (CI/CD)


## 🗂️ Project Structure

| Directory                     | Description                                               |
|-------------------------------|-----------------------------------------------------------|
| `weather-streaming-project/`  | Root project directory                                    |
| ├── `.github/`                | GitHub Actions for CI/CD                                  |
| │   ├── `workflows/`          | Contains CI/CD pipeline configurations                    |
| ├── `config/`                 | Stores configuration settings                             |
| │   ├── `__init__.py`         | Initialize the config package                             | 
| │   ├── `config.py`           | Stores API keys, Kafka, and DB settings                   |
| │   ├── `logger_config.py`    | Logger configuration                                      |
| ├── `ingestion/`              | Fetches and streams weather data                          |
| │   ├── `__init__.py`         | Initialize the ingestion package                          |
| │   ├── `weather_producer.py` | Fetches weather data from API & sends it to Kafka         |
| ├── `logs/`                   | Stores application logs                                   |
| │   ├── `app.log`             | Main log file                                             |
| ├── `processing/`             | Consumes and processes streamed data                      |
| │   ├── `__init__.py`         | Initialize the processing package                         |                         
| │   ├── `weather_consumer.py` | Consumes Kafka data & inserts into PostgreSQL             |
| ├── `storage/`                | Handles database and cloud storage operations             |
| │   ├── `__init__.py`         | Initialize the storage package                            |                                     
| │   ├── `database_setup.py`   | Creates PostgreSQL tables                                 |
| │   ├── `upload_to_gcs.py`    | Saves raw data to Google Cloud Storage (GCS)              |
| ├── `tests/`                  | Contains unit tests for the project                       |
| │   ├── `__init__.py`         | Initialize the tests package                              |
| │   ├── `test.py`             | Unit tests                                                |
| ├── `.env`                    | Stores API keys, database credentials (excluded from Git) |
| ├── `.gitignore`              | Excludes unnecessary files                                |
| ├── `LICENSE`                 | License information                                       |
| ├── `main.py`                 | Main script orchestrating tasks                           |
| ├── `README.md`               | Project documentation                                     |
| └── `requirements.txt`        | List of Python dependencies                               |

## 🚀 How to Get Started

## 🧪 Tests

## 🤝 Contributions

## 📜 License 
