import psycopg2
from psycopg2.extensions import connection as psycopg2_connection

from .base import DatabaseConnection

class PostgreSQLConnection(DatabaseConnection):
    def __init__(self, db_name, db_user, db_password, db_host="localhost", db_port="5432"):
        super().__init__(db_name, db_user, db_password, db_host, db_port)
        self.connection = None

    def get_db_connection(self) -> psycopg2_connection:
        """
        Establish and return a new connection to the PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            print("Database connection established successfully!")
            return self.connection
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            raise

    def save_event(self, pod_name, event_type, reason, message, timestamp):
        """
        Save an event to the database.
        """
        if not self.connection:
            self.get_db_connection()

        try:
            cursor = self.connection.cursor()
            # Ensure the table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pod_events (
                    id SERIAL PRIMARY KEY,
                    pod_name VARCHAR(255) NOT NULL,
                    event_type VARCHAR(50) NOT NULL,
                    reason VARCHAR(255),
                    message TEXT,
                    timestamp TIMESTAMP NOT NULL
                )
            """)
            self.connection.commit()

            # Insert the event
            cursor.execute("""
                INSERT INTO pod_events (pod_name, event_type, reason, message, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """, (pod_name, event_type, reason, message, timestamp))
            self.connection.commit()
            print(f"Event saved successfully: {pod_name}, {event_type}, {reason}, {message}, {timestamp}")
        except Exception as e:
            print(f"Failed to save event: {e}")
            raise
        finally:
            cursor.close()

    def close_connection(self):
        """
        Close the provided PostgreSQL connection.
        """
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
            self.connection = None
