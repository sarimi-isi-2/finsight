from fastapi import APIRouter
from pydantic import BaseModel, field_validator

from app.ml.predictor import predict_transaction


router = APIRouter()


class PredictionRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "Deskripsi transaksi tidak boleh kosong."
            )

        return value


@router.post("/predict")
def predict(request: PredictionRequest):

    result = predict_transaction(
        request.text
    )

    return {
        "text": request.text,
        "predicted_label": result
    }