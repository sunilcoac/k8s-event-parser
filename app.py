import uvicorn
import killport
from src.views.server import app

if __name__ == "__main__":
    killport.kill_ports(ports=[8000])
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
    
    
