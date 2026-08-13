from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    BASE_DIR
    / "data"
    / "final"
    / "merged_dataset.csv"
)

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
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
encoder = joblib.load(ENCODER_PATH)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(DATASET_PATH)

df = df.dropna(
    subset=[
        "text",
        "label"
    ]
)

X = df["text"].astype(str)
y = df["label"].astype(str)


# ============================================================
# ENCODE LABEL
# ============================================================

y_encoded = encoder.transform(y)


# ============================================================
# SPLIT DATASET
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


# ============================================================
# TF-IDF
# ============================================================

X_test_tfidf = vectorizer.transform(
    X_test
)


# ============================================================
# PREDICT
# ============================================================

y_pred = model.predict(
    X_test_tfidf
)


# ============================================================
# ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n========================================")
print("FINAL MODEL EVALUATION")
print("========================================")

print(
    f"\nAccuracy: {accuracy:.4f}"
)

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n========================================")
print("CLASSIFICATION REPORT")
print("========================================")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=encoder.classes_,
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("\n========================================")
print("CONFUSION MATRIX")
print("========================================")

cm = confusion_matrix(
    y_test,
    y_pred
)

cm_df = pd.DataFrame(
    cm,
    index=encoder.classes_,
    columns=encoder.classes_
)

print(cm_df)