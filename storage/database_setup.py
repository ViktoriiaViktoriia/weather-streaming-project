import psycopg2

from config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, logger


def create_connection():
    """Create and return a PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logger.info(f"Successfully connected to database: {DB_NAME} on {DB_HOST}:{DB_PORT}")
        return conn
    except Exception as e:
        logger.info(f"Error: Unable to connect to the database. {e}")
        return None


def close_connection(conn):
    """Close the database connection."""
    if conn:
        conn.close()
        logger.info("Connection closed.")


def execute_query(query, params=None):
    """Execute a SQL query."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            logger.info("The query executed successfully.")
            return result
        except Exception as e:
            logger.info(f"Error executing query: {e}")
            return None
        finally:
            close_connection(conn)


def insert_many(query, data_list):
    """Insert many rows using executemany()."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.executemany(query, data_list)
            conn.commit()
            cursor.close()
            logger.info(f"{len(data_list)} rows inserted.")
        except Exception as e:
            logger.error(f"Error in bulk insert: {e}")
            conn.rollback()
        finally:
            close_connection(conn)

