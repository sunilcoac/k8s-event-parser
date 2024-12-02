from fastapi import APIRouter
from src.controller.health_controller import HealthController

router = APIRouter()

@router.get("/health")
def health_check():
    status = HealthController.get_health_status()
    return status

