from fastapi import FastAPI

from app.routes.predict import router as predict_router
from app.routes.feedback import router as feedback_router
from app.routes.health import router as health_router


app = FastAPI(
    title="FinSight AI Service",
    version="1.0.0"
)


app.include_router(health_router)
app.include_router(predict_router)
app.include_router(feedback_router)