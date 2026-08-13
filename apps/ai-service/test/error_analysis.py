from pathlib import Path

import pandas as pd
import joblib

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

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
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
encoder = joblib.load(ENCODER_PATH)


# ============================================================
# ENCODE LABEL
# ============================================================

y_encoded = encoder.transform(y)


# ============================================================
# SPLIT DATA
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


# ============================================================
# PREDICT
# ============================================================

X_test_tfidf = vectorizer.transform(X_test)

y_pred = model.predict(X_test_tfidf)


# ============================================================
# ERROR ANALYSIS
# ============================================================

results = pd.DataFrame({
    "text": X_test.values,
    "actual": encoder.inverse_transform(y_test),
    "predicted": encoder.inverse_transform(y_pred)
})


errors = results[
    results["actual"] != results["predicted"]
].copy()


print("\n=== ERROR ANALYSIS ===")

print(
    f"Total test data : {len(results)}"
)

print(
    f"Total errors    : {len(errors)}"
)


# ============================================================
# TOP CONFUSIONS
# ============================================================

print("\n=== TOP CONFUSIONS ===")

confusions = (
    errors
    .groupby(
        ["actual", "predicted"]
    )
    .size()
    .reset_index(name="count")
    .sort_values(
        "count",
        ascending=False
    )
)

print(confusions.to_string(index=False))


# ============================================================
# ERROR EXAMPLES
# ============================================================

print("\n=== ERROR EXAMPLES ===")

print(
    errors[
        [
            "text",
            "actual",
            "predicted"
        ]
    ]
    .head(30)
    .to_string(index=False)
)