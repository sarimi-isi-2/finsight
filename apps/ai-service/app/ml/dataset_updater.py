from pathlib import Path
import pandas as pd


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MERGED_DATASET_PATH = (
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
# UPDATE DATASET
# ============================================================

def update_dataset():

    # 1. Cek file
    if not MERGED_DATASET_PATH.exists():
        return {
            "status": "error",
            "message": "merged_dataset.csv tidak ditemukan."
        }

    if not FEEDBACK_DATASET_PATH.exists():
        return {
            "status": "error",
            "message": "feedback_dataset.csv tidak ditemukan."
        }

    # 2. Load dataset
    merged_df = pd.read_csv(
        MERGED_DATASET_PATH
    )

    feedback_df = pd.read_csv(
        FEEDBACK_DATASET_PATH
    )

    # 3. Bersihkan nama kolom
    merged_df.columns = (
        merged_df.columns
        .str.strip()
    )

    feedback_df.columns = (
        feedback_df.columns
        .str.strip()
    )

    # 4. Pastikan kolom penting tersedia
    required_feedback_columns = [
    "text",
    "predicted_label",
    "corrected_label"
]

    for column in required_feedback_columns:

        if column not in feedback_df.columns:

            return {
                "status": "error",
                "message": (
                    f"Kolom '{column}' "
                    "tidak ditemukan di feedback."
                )
            }

    # 5. Ambil feedback yang punya corrected label
    feedback_clean = feedback_df[
    (
        feedback_df["corrected_label"].notna()
    )
    &
    (
        feedback_df["predicted_label"]
        != feedback_df["corrected_label"]
    )
].copy()

    feedback_clean["text"] = (
        feedback_clean["text"]
        .astype(str)
        .str.strip()
    )

    feedback_clean["corrected_label"] = (
        feedback_clean["corrected_label"]
        .astype(str)
        .str.strip()
    )

    # 6. Dataset lama
    dataset_before = len(merged_df)

    # 7. Cegah duplikasi berdasarkan text
    existing_texts = set(
        merged_df["text"]
        .astype(str)
        .str.strip()
    )

    new_rows = []

    for _, row in feedback_clean.iterrows():

        text = row["text"]
        label = row["corrected_label"]

        if text not in existing_texts:

            new_rows.append({
                "text": text,
                "label": label
            })

            existing_texts.add(text)

    # 8. Tambahkan data baru
    if new_rows:

        new_df = pd.DataFrame(
            new_rows
        )

        merged_df = pd.concat(
            [
                merged_df,
                new_df
            ],
            ignore_index=True
        )

        merged_df.to_csv(
            MERGED_DATASET_PATH,
            index=False
        )

    # 9. Hasil
    dataset_after = len(merged_df)

    return {
        "status": "success",
        "message": "Dataset berhasil diperiksa.",
        "added": dataset_after - dataset_before,
        "dataset_size": dataset_after
    }