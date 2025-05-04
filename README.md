# 📌 Project: Real-Time Weather Streaming with Kafka, GCS, and PostgreSQL


## 🚀 Overview
This project implements an ELT data pipeline that fetches weather data from the OpenWeather API,  
streams it using Apache Kafka, stores the raw data in Google Cloud Storage (GCS),  
transforms it, and then saves it into a PostgreSQL database for analysis.


## 🔹 Features
- Live weather data retrieval: Fetches up-to-date weather data from the OpenWeather API.
- Near real-time data streaming: Streams weather data from OpenWeather API with periodic updates using Kafka.
- Cloud storage simulation: Stores raw data in GCS, imitating large-scale data pipelines while staying within 
  free-tier limits.
- ELT process: Transforms and inserts structured data into PostgreSQL, simulating real-world data workflows.
- Scalable database design: Implements partitioning in PostgreSQL to optimize queries, improve performance by 
  limiting scans to only relevant partitions based on city and type filters, and prepare for future data growth.
- SQL-Based weather analysis: Allows easy SQL queries to analyze weather trends and patterns.
- Automated workflows: Uses CI/CD pipelines for continuous integration, automated testing, and deployment.


## 📦 Tech Stack
- Python (Data ingestion & processing)
- Kafka (Streaming pipeline)
- GCS (Raw data storage)
- PostgreSQL (Database storage & analysis)
- Pytest (Unit testing)
- GitHub Actions (CI/CD)


## 🗂️ Project Structure

| Directory / File                     | Description                                                                             |
|--------------------------------------|-----------------------------------------------------------------------------------------|
| `weather-streaming-project/`         | Root project directory                                                                  |
| ├── `.github/`                       | GitHub Actions for CI/CD                                                                |
| │   ├── `workflows/`                 | Contains CI/CD pipeline configurations                                                  |
| │   │    ├── `test.yml`              | Runs Python unit tests                                                                  |
| ├── `config/`                        | Stores configuration settings                                                           |
| │   ├── `__init__.py`                | Initialize the config package                                                           | 
| │   ├── `config.py`                  | Stores API keys, Kafka, and DB settings                                                 |
| │   ├── `logger_config.py`           | Logger configuration                                                                    |
| ├── `ingestion/`                     | Fetches and streams weather data                                                        |
| │   ├── `__init__.py`                | Initialize the ingestion package                                                        |
| │   ├── `weather_producer.py`        | Fetches weather data from API & sends it to Kafka topic                                 |
| ├── `logs/`                          | Stores application logs                                                                 |
| │   ├── `app.log`                    | Main log file                                                                           |
| ├── `processing/`                    | Consumes and processes streamed data                                                    |
| │   ├── `__init__.py`                | Initialize the processing package                                                       |                         
| │   ├── `weather_consumer.py`        | Listens to the Kafka topic, subscribes to the weather data & and writes raw data to GCS |
| │   ├── `weather_processing.py`      | Fetch data from GCS, process it, and then store the results in PostgreSQL               | 
| ├── `storage/`                       | Handles database and cloud storage operations                                           |
| │   ├── `__init__.py`                | Initialize the storage package                                                          |                                     
| │   ├── `database_setup.py`          | Creates PostgreSQL tables                                                               |
| │   ├── `upload_to_gcs.py`           | Saves raw data to Google Cloud Storage (GCS)                                            |
| ├── `tests/`                         | Contains unit tests for the project                                                     |
| │   ├── `__init__.py`                | Initialize the tests package                                                            |
| │   ├── `test_gcs_client_access.py`  | Tests access to Google Cloud Storage                                                    |
| │   ├── `test_weather_consumer.py`   | Unit tests: consumer                                                                    |
| │   ├── `test_weather_processing.py` | Unit tests: data processing and insert to database                                      |
| │   ├── `test_weather_producer.py`   | Unit tests: producer                                                                    |
| ├── `.env`                           | Stores API keys, database credentials (excluded from Git)                               |
| ├── `.gitignore`                     | Excludes unnecessary files                                                              |
| ├── `LICENSE`                        | License information                                                                     |
| ├── `main.py`                        | Main script orchestrating tasks                                                         |
| ├── `README.md`                      | Project documentation                                                                   |
| └── `requirements.txt`               | List of Python dependencies                                                             |

## 🚀 How to Get Started
**1. Clone the Repository**
   ```bash
   git clone https://github.com/ViktoriiaViktoriia/weather-streaming-project.git
   cd weather-streaming-project
   ```
**2. Install Dependencies**
   1. Set up a virtual environment:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
   2. Install Python dependencies:
      ```bash
      pip install -r requirements.txt
      ```
   3. Install required system packages:
      ```bash
      # Update package list
      sudo apt update && sudo apt upgrade -y

      # Install PostgreSQL (Database)
      sudo apt install -y postgresql postgresql-contrib

      # Install Kafka (Streaming Platform)
      # Go to: https://kafka.apache.org/downloads
      # Choose a version (e.g., Kafka 3.9.0 with Scala 2.13)
      # Under "Binary downloads", click the suggested mirror: kafka_2.13-3.9.0.tgz
      tar -xzf kafka_2.13-3.9.0.tgz
      mv kafka_2.13-3.9.0 kafka
      
      sudo apt install -y default-jdk  # Kafka requires Java
 
      sudo mv kafka /opt/
      rm kafka_2.13-3.9.0.tgz
      
      # Set correct permissions
      sudo chown -R $USER:$USER /opt/kafka
      chmod -R 755 /opt/kafka
      
      # Update environment variables
      echo 'export PATH=$PATH:/opt/kafka/bin' >> ~/.bashrc
      source ~/.bashrc

      # Install additional dev tools for better process management(optional)
      sudo apt install -y tmux htop unzip
      ```
**3. Run the pipeline:**
   ```bash
      # Start PostgreSQL
      sudo service postgresql start
      
      # Start Zookeeper first:
      zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
      
      #Then in a new terminal start Kafka:
      kafka-server-start.sh /opt/kafka/config/server.properties
      
      # Verify Kafka is running
      ps aux | grep '[k]afka'
      ps aux | grep '[z]ookeeper'
      
      # Check logs:
      tail -f /opt/kafka/logs/server.log

      # Stop running Kafka (if needed)
      /opt/kafka/bin/kafka-server-stop.sh
      # Stop running ZooKeeper (if needed)
      /opt/kafka/bin/zookeeper-server-stop.sh

      # Restart Kafka
      /opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties
      
      # Create Partitioned Tables
      # Before running the main pipeline (main.py), you need to manually (only once) run a script 
      # to create partitioned tables and database indexes:
      PYTHONPATH=. storage/partition_setup.py
      
      # Once the database structure is initialized, run the main script:
      python -m main
   ```
## 🧪 Tests
To run all unit tests, use either of the following commands:
   ```bash
   python -m pytest
   ```
or: 
```bash
   pytest tests/
   ```
## 🧪 CI
Unit tests are automatically run via GitHub Actions on every push.  
📄 Workflow file: `.github/workflows/test.yml`

## 🤝 Contributions
Your feedback and contributions are welcome! Submit issues or pull requests to collaborate.

## 📜 License 
Licensed under the [Apache License 2.0](LICENSE)
