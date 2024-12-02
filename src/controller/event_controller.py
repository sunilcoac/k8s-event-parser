from fastapi import HTTPException
from src.database.access_postgres import PostgreSQLConnection
from src.event_parser.console_viewer import ConsoleView
from src.event_parser.event_manager import PodEventController
from src.config.config import settings



class EventParser:
    
    def pod_event(self, namespace: str):
        # Initialize the PostgreSQL connection using settings from the config
        model = PostgreSQLConnection(
            db_name=settings.postgres.POSTGRES_DB,
            db_user=settings.postgres.POSTGRES_USER,
            db_password=settings.postgres.POSTGRES_PASSWORD,
            db_host=settings.postgres.POSTGRES_HOST,
            db_port=settings.postgres.POSTGRES_PORT
        )
        
        # Initialize the view and controller
        view = ConsoleView()
        controller = PodEventController(model, view)
        
        try:
            # Fetch and process pod events for the provided namespace
            controller.log_pod_events_by_type(namespace)
            
            # If everything works successfully, return a response
            response = {
                "status": "success",
                "message": "Pod events parsed successfully"
            }
            return response, 200
        except Exception as e:
            # If an exception occurs, raise an HTTP exception with a 500 status code
            raise HTTPException(status_code=500, detail="Internal Server Error") from e
        finally:
            # Ensure the database connection is always closed after the operation
            model.close_connection()

