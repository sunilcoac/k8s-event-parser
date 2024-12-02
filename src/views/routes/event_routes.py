from fastapi import APIRouter, HTTPException
from src.controller.event_controller import EventParser
from src.schemas.pod_event import NamespaceModel, ResponseModel

router = APIRouter()
event_parser = EventParser()

@router.post("/parse-pod-events", response_model=ResponseModel)
def parse_pod_events(data: NamespaceModel):
    """
    Parse pod events from the specified Kubernetes namespace.
    """
    try:
        response, status_code = event_parser.pod_event(data.namespace)
        
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
