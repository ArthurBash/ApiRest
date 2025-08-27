from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {
        "message": "User Management Microservice",
        "version": "1.0.0",
        "status": "active"
    }

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "user-microservice"
    }
