from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "ai-service",
        "version": "1.0.0"
    }