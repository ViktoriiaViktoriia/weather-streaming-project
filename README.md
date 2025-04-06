# 📌 Project: Real-Time Weather Streaming with Kafka & PostgreSQL


## 🚀 Overview
This project fetches weather data from OpenWeather API, streams it using Apache Kafka, and stores it 
in PostgreSQL for analysis.


## 🔹 Features
- Live weather data retrieval: Fetches up-to-date weather data from the OpenWeather API.
- Near real-time data streaming: Streams weather data from OpenWeather API with periodic updates using Kafka.
- Cloud storage simulation: Stores raw data in GCS, imitating large-scale data pipelines while staying within 
  free-tier limits.
- ETL process: Processes and loads data into PostgreSQL, simulating structured data transformation workflows.
- Scalable database design: Implements partitioning in PostgreSQL to optimize queries and prepare for future 
  data growth.
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

| Directory / File                | Description                                                                             |
|---------------------------------|-----------------------------------------------------------------------------------------|
| `weather-streaming-project/`    | Root project directory                                                                  |
| ├── `.github/`                  | GitHub Actions for CI/CD                                                                |
| │   ├── `workflows/`            | Contains CI/CD pipeline configurations                                                  |
| ├── `config/`                   | Stores configuration settings                                                           |
| │   ├── `__init__.py`           | Initialize the config package                                                           | 
| │   ├── `config.py`             | Stores API keys, Kafka, and DB settings                                                 |
| │   ├── `logger_config.py`      | Logger configuration                                                                    |
| ├── `ingestion/`                | Fetches and streams weather data                                                        |
| │   ├── `__init__.py`           | Initialize the ingestion package                                                        |
| │   ├── `weather_producer.py`   | Fetches weather data from API & sends it to Kafka topic                                 |
| ├── `logs/`                     | Stores application logs                                                                 |
| │   ├── `app.log`               | Main log file                                                                           |
| ├── `processing/`               | Consumes and processes streamed data                                                    |
| │   ├── `__init__.py`           | Initialize the processing package                                                       |                         
| │   ├── `weather_consumer.py`   | Listens to the Kafka topic, subscribes to the weather data & and writes raw data to GCS |
| │   ├── `weather_processing.py` | Fetch data from GCS, process it, and then store the results in PostgreSQL               | 
| ├── `storage/`                  | Handles database and cloud storage operations                                           |
| │   ├── `__init__.py`           | Initialize the storage package                                                          |                                     
| │   ├── `database_setup.py`     | Creates PostgreSQL tables                                                               |
| │   ├── `upload_to_gcs.py`      | Saves raw data to Google Cloud Storage (GCS)                                            |
| ├── `tests/`                    | Contains unit tests for the project                                                     |
| │   ├── `__init__.py`           | Initialize the tests package                                                            |
| │   ├── `test.py`               | Unit tests                                                                              |
| ├── `.env`                      | Stores API keys, database credentials (excluded from Git)                               |
| ├── `.gitignore`                | Excludes unnecessary files                                                              |
| ├── `LICENSE`                   | License information                                                                     |
| ├── `main.py`                   | Main script orchestrating tasks                                                         |
| ├── `README.md`                 | Project documentation                                                                   |
| └── `requirements.txt`          | List of Python dependencies                                                             |

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
      sudo apt install -y default-jdk  # Kafka requires Java
      wget https://dlcdn.apache.org/kafka/3.9.0/kafka-3.9.0-src.tgz
      tar -xvzf kafka-3.9.0-src.tgz
      sudo mv kafka-3.9.0-src /opt/kafka
      rm kafka-3.9.0-src.tgz
      
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
      
      # Start Kafka from /opt/kafka
      # Start Zookeeper first
      /opt/kafka/bin/zookeeper-server-start.sh -daemon /opt/kafka/config/zookeeper.properties
      #Then start Kafka
      /opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties
      
      # Verify Kafka is running
      ps aux | grep kafka
      ps aux | grep zookeeper

      # Check logs:
      tail -f /opt/kafka/logs/server.log

      # Stop running Kafka (if needed)
      /opt/kafka/bin/kafka-server-stop.sh
      # Stop running ZooKeeper (if needed)
      /opt/kafka/bin/zookeeper-server-stop.sh

      # Restart Kafka
      /opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties
      
      # Run the main script
      python -m main
   ```
## 🧪 Tests
Run unit tests with:
   ```bash
   python -m pytest
   ```

## 🤝 Contributions
Your feedback and contributions are welcome! Submit issues or pull requests to collaborate.

## 📜 License 
Licensed under the [Apache License 2.0](LICENSE)
