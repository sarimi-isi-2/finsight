from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
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

FEEDBACK_DATASET_PATH = (
    BASE_DIR
    / "data"
    / "final"
    / "feedback_dataset.csv"
)


# ============================================================
# RETRAIN MODEL
# ============================================================

def retrain_model():

    # --------------------------------------------------------
    # 1. Load dataset
    # --------------------------------------------------------

    df = pd.read_csv(
        DATASET_PATH
    )

    # --------------------------------------------------------
    # 2. Bersihkan data kosong
    # --------------------------------------------------------

    df = df.dropna(
        subset=[
            "text",
            "label"
        ]
    )

        # --------------------------------------------------------
    # 3. Pisahkan input dan target
    # --------------------------------------------------------

    X = df["text"].astype(str)
    y = df["label"].astype(str)

    # --------------------------------------------------------
    # 4. Encode label
    # --------------------------------------------------------

    encoder = LabelEncoder()

    y_encoded = encoder.fit_transform(
        y
    )

    # --------------------------------------------------------
    # 5. Split dataset utama
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y_encoded,
            test_size=0.2,
            random_state=42,
            stratify=y_encoded
        )
    )

    # --------------------------------------------------------
    # 5A. Tambahkan feedback langsung ke TRAINING
    # --------------------------------------------------------

    feedback_clean = pd.DataFrame()

    if FEEDBACK_DATASET_PATH.exists():

        feedback_df = pd.read_csv(
            FEEDBACK_DATASET_PATH
        )

        feedback_df.columns = (
            feedback_df.columns
            .str.strip()
        )

        required_columns = [
            "text",
            "predicted_label",
            "corrected_label"
        ]

        if all(
            column in feedback_df.columns
            for column in required_columns
        ):

            feedback_clean = feedback_df[
                (
                    feedback_df["predicted_label"]
                    != feedback_df["corrected_label"]
                )
            ].dropna(
                subset=[
                    "text",
                    "corrected_label"
                ]
            )

            if len(feedback_clean) > 0:

                feedback_X = (
                    feedback_clean["text"]
                    .astype(str)
                    .str.strip()
                )

                feedback_y = (
                    feedback_clean["corrected_label"]
                    .astype(str)
                    .str.strip()
                )

                feedback_encoded = (
                    encoder.transform(
                        feedback_y
                    )
                )

                X_train = pd.concat(
                    [
                        X_train,
                        feedback_X
                    ],
                    ignore_index=True
                )

                y_train = pd.concat(
                    [
                        pd.Series(
                            y_train
                        ),
                        pd.Series(
                            feedback_encoded
                        )
                    ],
                    ignore_index=True
                )

                print(
                    f"Feedback ditambahkan ke TRAINING: "
                    f"{len(feedback_clean)} data"
                )

    # --------------------------------------------------------
    # 6. TF-IDF
    # --------------------------------------------------------

    vectorizer = TfidfVectorizer()

    X_train_tfidf = (
        vectorizer.fit_transform(
            X_train
        )
    )

    X_test_tfidf = (
        vectorizer.transform(
            X_test
        )
    )

    # --------------------------------------------------------
    # 7. Train SVM
    # --------------------------------------------------------

    svm = LinearSVC()

    svm.fit(
        X_train_tfidf,
        y_train
    )

    # --------------------------------------------------------
    # 8. Evaluasi global
    # --------------------------------------------------------

    y_pred = svm.predict(
        X_test_tfidf
    )

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    print(
        f"Accuracy model baru: {accuracy:.4f}"
    )

        # --------------------------------------------------------
    # 9. Evaluasi feedback
    # --------------------------------------------------------

    feedback_accuracy = None
    feedback_count = len(feedback_clean)

    if len(feedback_clean) > 0:

        feedback_text = (
            feedback_clean["text"]
            .astype(str)
            .str.strip()
        )

        feedback_labels = (
            feedback_clean["corrected_label"]
            .astype(str)
            .str.strip()
        )

        feedback_tfidf = (
            vectorizer.transform(
                feedback_text
            )
        )

        feedback_encoded = (
            encoder.transform(
                feedback_labels
            )
        )

        feedback_pred = svm.predict(
            feedback_tfidf
        )

        feedback_accuracy = (
            accuracy_score(
                feedback_encoded,
                feedback_pred
            )
        )

        print(
            "Feedback accuracy model baru: "
            f"{feedback_accuracy:.4f}"
        )

    # --------------------------------------------------------
    # 10. Return
    # --------------------------------------------------------

    return {
        "status": "success",
        "accuracy": accuracy,
        "feedback_accuracy": feedback_accuracy,
        "feedback_count": feedback_count,
        "dataset_size": len(X),
        "model": svm,
        "vectorizer": vectorizer,
        "encoder": encoder
    }