from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.predict import router as predict_router
from app.routes.feedback import router as feedback_router
from app.routes.health import router as health_router


app = FastAPI(
    title="FinSight AI Service",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTES
# ============================================================

app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    predict_router,
    prefix="/api/v1"
)

app.include_router(
    feedback_router,
    prefix="/api/v1"
)