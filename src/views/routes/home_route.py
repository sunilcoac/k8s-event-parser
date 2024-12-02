from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=str)
def get_home():
    return "Welcome to the API!"
