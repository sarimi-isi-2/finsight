from pathlib import Path
import joblib


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "models" / "vectorizer.pkl"
ENCODER_PATH = BASE_DIR / "models" / "label_encoder.pkl"


model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
encoder = joblib.load(ENCODER_PATH)


# ============================================================
# RULE-BASED KEYWORDS
# ============================================================

INCOME_KEYWORDS = [
    "payroll",
    "salary received",
    "gaji",
    "bonus",
    "thr",
    "honorarium",
    "insentif",
    "komisi penjualan",
    "pendapatan freelance",
]


def predict_transaction(text: str):

    text_clean = text.lower().strip()

    # --------------------------------------------------------
    # 1. Rule-based override
    # --------------------------------------------------------

    # "potongan admin payroll" bukan income
    if "potongan" in text_clean and "payroll" in text_clean:
        return "fees"

    for keyword in INCOME_KEYWORDS:
        if keyword in text_clean:
            return "income"

    # --------------------------------------------------------
    # 2. ML prediction
    # --------------------------------------------------------

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)

    label = encoder.inverse_transform(prediction)

    return label[0]