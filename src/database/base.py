from abc import ABC, abstractmethod

class DatabaseConnection(ABC):
    def __init__(self, db_name, db_user, db_password, db_host="localhost", db_port="5432"):
        """
        Initialize the database connection parameters.
        """
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    @abstractmethod
    def get_db_connection(self):
        """
        Return a database connection object.
        This method must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def save_event(self, pod_name, event_type, reason, mesage, timestamp):
        """
        Save an event to the database
        """
        pass 
    
    @abstractmethod
    def close_connection(self, connection):
        """
        Close the provided database connection.
        This method must be implemented by subclasses.
        """
        pass
