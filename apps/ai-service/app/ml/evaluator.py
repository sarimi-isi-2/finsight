from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR
    / "data"
    / "final"
    / "merged_dataset.csv"
)


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(
    model,
    vectorizer,
    encoder
):

    # 1. Load dataset
    df = pd.read_csv(
        DATASET_PATH
    )

    # 2. Bersihkan data
    df = df.dropna(
        subset=[
            "text",
            "label"
        ]
    )

    # 3. Input dan target
    X = df["text"].astype(str)
    y = df["label"].astype(str)

    # 4. Encode label
    y_encoded = encoder.transform(y)

    # 5. Split dataset
    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y_encoded,
            test_size=0.2,
            random_state=42,
            stratify=y_encoded
        )
    )

    # 6. Vectorize TEST DATA
    X_test_tfidf = vectorizer.transform(
        X_test
    )

    # 7. Predict
    y_pred = model.predict(
        X_test_tfidf
    )

    # 8. Accuracy
    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    return accuracy