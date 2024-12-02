from fastapi import HTTPException

class HealthController:
    @staticmethod
    def get_health_status():
        try:
            return {"status": "healthy", "message": "Service is running"}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error") from e