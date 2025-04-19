import os
import pandas as pd
import shutil

from config import logger
from storage import execute_query, insert_many


def process_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and format the raw weather DataFrame."""
    df = df.copy()

    # Example cleaning steps
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
    df['city'] = df['city'].str.title().str.strip()

    df.drop_duplicates(subset=['city', 'timestamp'], inplace=True)

    # Drop rows with missing essential values
    df.dropna(subset=['timestamp', 'city', 'temperature'], inplace=True)

    # Convert Kelvin to Celsius:
    df['temperature'] = (df['temperature'] - 273.15).round(2)
    df['feels_like'] = (df['feels_like'] - 273.15).round(2)

    return df


def insert_weather_data(df: pd.DataFrame):
    """Insert processed weather data into PostgreSQL database."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        type TEXT,
        city TEXT,
        description TEXT,
        temperature REAL,
        feels_like REAL,
        humidity INT,
        wind REAL,
        pressure INT,
        timestamp TIMESTAMP
    );
    """

    insert_query = """
    INSERT INTO weather_data (
        type, city, description, temperature,
        feels_like, humidity, wind, pressure, timestamp
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    try:
        # Create table if not exists
        execute_query(create_table_query)

        # Convert DataFrame to list of tuples
        data_list = [
            (
                row['type'], row['city'], row['description'], row['temperature'],
                row['feels_like'], row['humidity'], row['wind'], row['pressure'],
                row['timestamp']
            )
            for _, row in df.iterrows()
        ]

        if data_list:  # avoid inserting empty data
            # Bulk insert
            insert_many(insert_query, data_list)
        else:
            logger.warning("DataFrame is empty. No data to insert.")

    except Exception as e:
        logger.error(f"Error inserting data into PostgreSQL: {e}")


def load_all_csvs(raw_data_folder_path, processed_data_folder_path):
    all_dfs = []

    try:
        for filename in os.listdir(raw_data_folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(raw_data_folder_path, filename)

                try:
                    df = pd.read_csv(file_path)
                    all_dfs.append(df)

                    # Move file after successful read
                    shutil.move(file_path, os.path.join(processed_data_folder_path, filename))
                    logger.info(f" Moved {filename} to processed folder.")

                except Exception as e:
                    logger.error(f" Failed to read {file_path}: {e}")

        if all_dfs:
            combined_df = pd.concat(all_dfs, ignore_index=True)

            processed_df = process_weather_data(combined_df)

            insert_weather_data(processed_df)

            logger.info(" Successfully processed and inserted data.")

            return processed_df

        else:
            logger.info(" No CSV files to process.")
            return pd.DataFrame()

    except Exception as e:
        logger.error(f" Error processing all CSVs: {e}")
        return pd.DataFrame()

