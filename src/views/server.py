from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.views.routes.home_route import router as home_router
from src.views.routes.api_health import router as api_health_router
from src.views.routes.event_routes import router as event_router 

def get_application() -> FastAPI:
    """
    Function to initialize the FastAPI application.
    """
    
    _app = FastAPI(
        title="COAC Pod Event Manager",
    )
    
    # CORS settings 
    
    origins = [
        "*",
        "http://localhost",
        "http://localhost:8000"
    ]
    
    # Middleware setup to handle CORS requests
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return _app

# Initialize the FastAPI Application
app = get_application()

# Print statement for loading indicator
print("Loading routes... This may take a while")

# Include the routers
app.include_router(home_router, tags=["Home"])
app.include_router(api_health_router, tags=["API Health"])
app.include_router(event_router, tags=["Pod Event"])

