"""
This script initializes partitioned tables in the PostgreSQL database.

Usage:
    Run manually once before starting the main pipeline:
        $ PYTHONPATH=. storage/partition_setup.py
"""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from config import engine, logger, CITIES, KAFKA_TOPIC, KAFKA_TOPIC_FORECAST


def create_partitioned_table():
    """Create parent partitioned table and child partitions."""

    types = [KAFKA_TOPIC, KAFKA_TOPIC_FORECAST]

    try:
        with engine.begin() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS weather_data_partition (
                    id SERIAL,
                    type TEXT NOT NULL,
                    city TEXT NOT NULL,
                    description TEXT,
                    temperature REAL,
                    feels_like REAL,
                    humidity INT,
                    wind REAL,
                    pressure INT,
                    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (id, city, type),
                    UNIQUE (city, type, timestamp),
                    CONSTRAINT weather_data_partition_city_type CHECK (city IS NOT NULL AND type IS NOT NULL)
                ) PARTITION BY LIST (city);
            """))

            # Verify parent table exists
            result = connection.execute(text("""
                SELECT to_regclass('public.weather_data_partition');
            """)).scalar()

            if result is None:
                logger.error("Parent table 'weather_data_partition' was not created!")
                raise RuntimeError("Partitioned table creation failed.")
            else:
                logger.info("Parent partitioned table 'weather_data_partition' created successfully.")

                for city in CITIES:
                    try:
                        # Create partition for each city
                        create_city_partition_query = f"""
                            CREATE TABLE IF NOT EXISTS weather_data_{city.lower()}
                            PARTITION OF weather_data_partition
                            FOR VALUES IN ('{city}')
                            PARTITION BY LIST (type);
                        """
                        # Execute the query for each city
                        connection.execute(text(create_city_partition_query))
                        logger.info(f"Partition created for city: {city}")
                    except SQLAlchemyError as e:
                        logger.error(f"Error creating city partition for '{city}': {e}")
                        raise

                    try:
                        #  Create type (topic) partitions inside each city partition
                        for weather_type in types:
                            partition_name = f"weather_data_{city.lower()}_{weather_type.split('_')[1]}"
                            create_type_partition_query = f"""
                                CREATE TABLE IF NOT EXISTS {partition_name}
                                PARTITION OF weather_data_{city.lower()}
                                FOR VALUES IN ('{weather_type}');
                            """

                            # Execute the query for each type
                            connection.execute(text(create_type_partition_query))
                            logger.info(f"Partition created for type: {weather_type}")

                            index_type_partition_query = f"""
                                CREATE INDEX IF NOT EXISTS idx_{city.lower()}_city_{weather_type.split('_')[1]}
                                ON {partition_name}(city, type, timestamp);
                            """

                            # Execute the query for each type
                            connection.execute(text(index_type_partition_query))
                            logger.info(f"Indexes were created for type: {weather_type}, city: {city}")

                    except SQLAlchemyError as e:
                        logger.error(f"Error creating type partition for '{city}' and type '{weather_type}': {e}")
                        raise

                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS weather_data_other
                    PARTITION OF weather_data_partition
                    DEFAULT;
                """))

                connection.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_other_city_type 
                    ON weather_data_other(city, type, timestamp);
                """))

                logger.info(" Partitioned table and child tables created successfully.")

    except Exception as e:
        # Log any errors that occur
        logger.error(f"An error occurred while creating partitions: {e}")
        # Stop execution by re-raising the exception
        raise  # This stops further execution and propagates the error


def migrate_data():
    """Migrate existing data from weather_data into weather_data_partition."""

    try:
        with engine.begin() as connection:
            logger.info("Starting data migration to partitioned table...")

            # Check if partitioned table already has data
            result = connection.execute(text("SELECT COUNT(*) FROM weather_data_partition;"))
            count = result.scalar()  # Get single number

            if count > 0:
                logger.info("Partitioned table already contains data. Skipping migration.")
                return  # Exit the function if already migrated

            # If empty, insert data
            result = connection.execute(text("""
                INSERT INTO weather_data_partition (type, city, description, temperature, feels_like, 
                humidity, wind, pressure, timestamp)
                SELECT type, city, description, temperature, feels_like, humidity, wind, pressure, timestamp
                FROM weather_data
                ON CONFLICT (city, type, timestamp) DO NOTHING;
            """))
            logger.info(f"{result.rowcount} rows migrated from weather_data to weather_data_partition.")
            logger.info("Data migrated successfully to weather_data_partition.")

    except Exception as e:
        logger.error(f"Error during data migration: {e}")
        raise  # Stop the process if migration fails


if __name__ == "__main__":
    create_partitioned_table()
    migrate_data()

