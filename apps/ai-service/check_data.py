import pandas as pd
import joblib

# =========================
# CEK MERGED DATASET
# =========================

df = pd.read_csv("data/final/merged_dataset.csv")

print("=== MERGED DATASET ===")
print("Dataset size:", len(df))

print("\nCategories:")
print(df["label"].value_counts())

# =========================
# CEK FEEDBACK
# =========================

feedback = pd.read_csv(
    "data/final/feedback_dataset.csv"
)

print("\n=== FEEDBACK ===")
print("Total feedback:", len(feedback))

wrong_feedback = (
    feedback["predicted_label"]
    != feedback["corrected_label"]
)

print(
    "Jumlah feedback salah:",
    wrong_feedback.sum()
)

# =========================
# CEK ENCODER
# =========================

encoder = joblib.load(
    "models/label_encoder.pkl"
)

print("\n=== LABEL ENCODER ===")
print("Encoder classes:")

for label in encoder.classes_:
    print("-", label)

# =========================
# CEK PENDING FEEDBACK
# =========================

existing_texts = set(
    df["text"]
    .astype(str)
    .str.strip()
)

pending = feedback[
    (
        feedback["predicted_label"]
        != feedback["corrected_label"]
    )
    &
    (
        ~feedback["text"]
        .astype(str)
        .str.strip()
        .isin(existing_texts)
    )
]

print("\n=== PENDING FEEDBACK ===")
print("Pending:", len(pending))

print("\nPending data:")
print(
    pending[
        [
            "text",
            "predicted_label",
            "corrected_label"
        ]
    ]
)