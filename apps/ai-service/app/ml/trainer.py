import joblib
import pandas as pd

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score


BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = BASE_DIR / "data" / "final" / "merged_dataset.csv"

MODEL_PATH = BASE_DIR / "models" / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "models" / "vectorizer.pkl"
ENCODER_PATH = BASE_DIR / "models" / "label_encoder.pkl"


def train_model():

    # =========================
    # 1. LOAD DATASET
    # =========================

    df = pd.read_csv(DATASET_PATH)

    X = df["text"].astype(str)
    y = df["label"].astype(str)


    # =========================
    # 2. SPLIT DATA
    # =========================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )


    # =========================
    # 3. LABEL ENCODING
    # =========================

    encoder = LabelEncoder()

    y_train_encoded = encoder.fit_transform(y_train)
    y_test_encoded = encoder.transform(y_test)


    # =========================
    # 4. TF-IDF
    # =========================

    vectorizer = TfidfVectorizer()

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)


    # =========================
    # 5. TRAIN SVM
    # =========================

    svm = LinearSVC()

    svm.fit(
        X_train_tfidf,
        y_train_encoded
    )


    # =========================
    # 6. EVALUATION
    # =========================

    y_pred = svm.predict(X_test_tfidf)

    accuracy = accuracy_score(
        y_test_encoded,
        y_pred
    )


    # =========================
    # 7. SAVE MODEL
    # =========================

    joblib.dump(
        svm,
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


    return {
        "accuracy": accuracy,
        "dataset_size": len(df)
    }