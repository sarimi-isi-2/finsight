from pathlib import Path

import joblib

from app.ml.retrainer import retrain_model


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "model.pkl"
)

VECTORIZER_PATH = (
    BASE_DIR
    / "models"
    / "vectorizer.pkl"
)

ENCODER_PATH = (
    BASE_DIR
    / "models"
    / "label_encoder.pkl"
)


# ============================================================
# LOAD CURRENT MODEL
# ============================================================

def load_current_model():

    model = joblib.load(
        MODEL_PATH
    )

    vectorizer = joblib.load(
        VECTORIZER_PATH
    )

    encoder = joblib.load(
        ENCODER_PATH
    )

    return (
        model,
        vectorizer,
        encoder
    )


# ============================================================
# SAVE MODEL
# ============================================================

def save_model(
    model,
    vectorizer,
    encoder
):

    joblib.dump(
        model,
        MODEL_PATH
    )

    joblib.dump(
        vectorizer,
        VECTORIZER_PATH
    )

    joblib.dump(
        encoder,
        ENCODER_PATH
    )


# ============================================================
# COMPARE ACCURACY
# ============================================================

def compare_accuracy(
    old_accuracy,
    new_accuracy,
    old_feedback_accuracy,
    new_feedback_accuracy
):

    MAX_ACCURACY_DROP = 0.005

    global_accuracy_improved = (
        new_accuracy > old_accuracy
    )

    global_accuracy_safe = (
        new_accuracy >= (
            old_accuracy
            - MAX_ACCURACY_DROP
        )
    )

    feedback_improved = False

    if (
        old_feedback_accuracy is not None
        and new_feedback_accuracy is not None
    ):
        feedback_improved = (
            new_feedback_accuracy
            > old_feedback_accuracy
        )

    # Model baru lebih bagus secara global
    if global_accuracy_improved:

        return {
            "update": True,
            "reason": "global_accuracy_improved",
            "message": (
                "Model baru memiliki "
                "global accuracy lebih tinggi."
            )
        }

    # Feedback membaik dan global accuracy
    # masih dalam batas aman
    if (
        feedback_improved
        and global_accuracy_safe
    ):

        return {
            "update": True,
            "reason": "feedback_improved",
            "message": (
                "Feedback accuracy meningkat "
                "dan penurunan global accuracy "
                "masih dalam batas aman."
            )
        }

    return {
        "update": False,
        "reason": "model_not_better",
        "message": (
            "Model baru tidak memenuhi "
            "kriteria update. "
            "Model lama dipertahankan."
        )
    }


# ============================================================
# RETRAIN + UPDATE
# ============================================================

def retrain_and_update():

    # --------------------------------------------------------
    # 1. Load model lama
    # --------------------------------------------------------

    old_model, old_vectorizer, old_encoder = (
        load_current_model()
    )

    # --------------------------------------------------------
    # 2. Evaluasi model lama
    # --------------------------------------------------------

    from app.ml.evaluator import evaluate_model

    old_accuracy = evaluate_model(
        old_model,
        old_vectorizer,
        old_encoder
    )

    # --------------------------------------------------------
    # 3. Train kandidat baru
    # --------------------------------------------------------

    result = retrain_model()

    new_model = result["model"]
    new_vectorizer = result["vectorizer"]
    new_encoder = result["encoder"]

    # --------------------------------------------------------
    # 4. Accuracy kandidat baru
    # --------------------------------------------------------

    new_accuracy = result["accuracy"]

    new_feedback_accuracy = (
        result["feedback_accuracy"]
    )

    feedback_count = (
        result["feedback_count"]
    )

    # --------------------------------------------------------
    # 5. Evaluasi feedback model lama
    # --------------------------------------------------------

    old_feedback_accuracy = None

    if feedback_count > 0:

        from sklearn.metrics import accuracy_score
        import pandas as pd

        feedback_path = (
            BASE_DIR
            / "data"
            / "final"
            / "feedback_dataset.csv"
        )

        if feedback_path.exists():

            feedback_df = pd.read_csv(
                feedback_path
            )

            feedback_df.columns = (
                feedback_df.columns
                .str.strip()
            )

            feedback_df = feedback_df[
                (
                    feedback_df[
                        "predicted_label"
                    ]
                    != feedback_df[
                        "corrected_label"
                    ]
                )
            ].dropna(
                subset=[
                    "text",
                    "corrected_label"
                ]
            )

            if len(feedback_df) > 0:

                feedback_text = (
                    feedback_df["text"]
                    .astype(str)
                    .str.strip()
                )

                feedback_labels = (
                    feedback_df[
                        "corrected_label"
                    ]
                    .astype(str)
                    .str.strip()
                )

                feedback_tfidf = (
                    old_vectorizer.transform(
                        feedback_text
                    )
                )

                feedback_encoded = (
                    old_encoder.transform(
                        feedback_labels
                    )
                )

                old_feedback_pred = (
                    old_model.predict(
                        feedback_tfidf
                    )
                )

                old_feedback_accuracy = (
                    accuracy_score(
                        feedback_encoded,
                        old_feedback_pred
                    )
                )

    # --------------------------------------------------------
    # 6. Compare
    # --------------------------------------------------------

    comparison = compare_accuracy(
        old_accuracy,
        new_accuracy,
        old_feedback_accuracy,
        new_feedback_accuracy
    )

    # --------------------------------------------------------
    # 7. Save model baru
    # --------------------------------------------------------

    if comparison["update"]:

        save_model(
            new_model,
            new_vectorizer,
            new_encoder
        )

        return {
            "status": "updated",
            "old_accuracy": old_accuracy,
            "new_accuracy": new_accuracy,
            "old_feedback_accuracy": (
                old_feedback_accuracy
            ),
            "new_feedback_accuracy": (
                new_feedback_accuracy
            ),
            "feedback_count": feedback_count,
            "reason": comparison["reason"],
            "message": (
                "Model baru berhasil disimpan."
            )
        }

    # --------------------------------------------------------
    # 8. Keep model lama
    # --------------------------------------------------------

    return {
        "status": "kept_old",
        "old_accuracy": old_accuracy,
        "new_accuracy": new_accuracy,
        "old_feedback_accuracy": (
            old_feedback_accuracy
        ),
        "new_feedback_accuracy": (
            new_feedback_accuracy
        ),
        "feedback_count": feedback_count,
        "reason": comparison["reason"],
        "message": (
            "Model lama dipertahankan."
        )
    }


# ============================================================
# PIPELINE
# ============================================================

def retrain_pipeline():

    return retrain_and_update()