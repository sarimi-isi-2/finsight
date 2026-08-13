from pathlib import Path

import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel, field_validator

from app.ml.dataset_updater import update_dataset
from app.ml.model_manager import retrain_pipeline


router = APIRouter()


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FEEDBACK_PATH = (
    BASE_DIR
    / "data"
    / "final"
    / "feedback_dataset.csv"
)

MERGED_DATASET_PATH = (
    BASE_DIR
    / "data"
    / "final"
    / "merged_dataset.csv"
)


# ============================================================
# CONFIG
# ============================================================

RETRAIN_THRESHOLD = 10


# ============================================================
# REQUEST MODEL
# ============================================================

VALID_CATEGORIES = {
    "shopping",
    "investment",
    "food",
    "travel",
    "loan",
    "transfer",
    "healthcare",
    "education",
    "bills",
    "entertainment",
    "topup",
    "donation",
    "transport",
    "income",
    "fees",
}

class FeedbackRequest(BaseModel):
    text: str
    predicted_label: str
    corrected_label: str

    @field_validator(
        "predicted_label",
        "corrected_label"
    )
    @classmethod
    def validate_category(cls, value: str):
        value = value.strip().lower()

        if value not in VALID_CATEGORIES:
            raise ValueError(
                f"Kategori tidak valid: {value}"
            )

        return value


# ============================================================
# FEEDBACK ENDPOINT
# ============================================================

@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):

    # --------------------------------------------------------
    # 1. Tentukan apakah prediksi benar
    # --------------------------------------------------------

    is_correct = (
        request.predicted_label
        == request.corrected_label
    )

    # --------------------------------------------------------
    # 2. Buat feedback baru
    # --------------------------------------------------------

    new_feedback = pd.DataFrame([
        {
            "text": request.text,
            "predicted_label": request.predicted_label,
            "corrected_label": request.corrected_label,
            "is_correct": is_correct
        }
    ])

    # --------------------------------------------------------
    # 3. Load feedback lama
    # --------------------------------------------------------

    if FEEDBACK_PATH.exists():

        feedback_df = pd.read_csv(
            FEEDBACK_PATH
        )

    else:

        feedback_df = pd.DataFrame(
            columns=[
                "text",
                "predicted_label",
                "corrected_label",
                "is_correct"
            ]
        )

    # --------------------------------------------------------
    # 4. Bersihkan nama kolom
    # --------------------------------------------------------

    feedback_df.columns = (
        feedback_df.columns
        .str.strip()
    )

    # --------------------------------------------------------
    # 5. Pastikan kolom is_correct tersedia
    # --------------------------------------------------------

    if "is_correct" not in feedback_df.columns:

        feedback_df["is_correct"] = (
            feedback_df["predicted_label"]
            == feedback_df["corrected_label"]
        )

    # --------------------------------------------------------
    # 6. Tambahkan feedback baru
    # --------------------------------------------------------

    feedback_df = pd.concat(
        [
            feedback_df,
            new_feedback
        ],
        ignore_index=True
    )

    # --------------------------------------------------------
    # 7. Hapus duplikat feedback
    # --------------------------------------------------------

    feedback_df = (
        feedback_df
        .drop_duplicates(
            subset=["text"],
            keep="last"
        )
    )

    # --------------------------------------------------------
    # 8. Simpan feedback
    # --------------------------------------------------------

    feedback_df.to_csv(
        FEEDBACK_PATH,
        index=False
    )

    # --------------------------------------------------------
    # 9. Load dataset utama
    # --------------------------------------------------------

    if MERGED_DATASET_PATH.exists():

        merged_df = pd.read_csv(
            MERGED_DATASET_PATH
        )

        merged_df.columns = (
            merged_df.columns
            .str.strip()
        )

        existing_texts = set(
            merged_df["text"]
            .astype(str)
            .str.strip()
        )

    else:

        existing_texts = set()

    # --------------------------------------------------------
    # 10. Cari feedback salah yang belum masuk dataset
    # --------------------------------------------------------

    pending_feedback = feedback_df[
        (
            feedback_df["predicted_label"]
            != feedback_df["corrected_label"]
        )
        &
        (
            ~feedback_df["text"]
            .astype(str)
            .str.strip()
            .isin(existing_texts)
        )
    ].copy()

    # --------------------------------------------------------
    # 11. Hilangkan duplikat berdasarkan text
    # --------------------------------------------------------

    pending_feedback = (
        pending_feedback
        .drop_duplicates(
            subset=["text"],
            keep="last"
        )
    )

    pending_count = len(
        pending_feedback
    )

    # --------------------------------------------------------
    # 12. Default hasil pipeline
    # --------------------------------------------------------

    dataset_result = None
    retrain_result = None

    # --------------------------------------------------------
    # 13. Jalankan pipeline jika threshold tercapai
    # --------------------------------------------------------

    if pending_count >= RETRAIN_THRESHOLD:

        dataset_result = update_dataset()

        retrain_result = retrain_pipeline()

    # --------------------------------------------------------
    # 14. Response
    # --------------------------------------------------------

    return {
        "status": "success",
        "message": "Feedback berhasil disimpan.",
        "feedback": {
            "text": request.text,
            "predicted_label": request.predicted_label,
            "corrected_label": request.corrected_label,
            "is_correct": is_correct
        },
        "pending_feedback": pending_count,
        "retrain_threshold": RETRAIN_THRESHOLD,
        "dataset_update": dataset_result,
        "retrain": retrain_result
    }