from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    BASE_DIR
    / "data"
    / "final"
    / "merged_dataset.csv"
)


df = pd.read_csv(DATASET_PATH)

df.columns = df.columns.str.strip()

categories = [
    "shopping",
    "food",
    "income",
    "healthcare",
    "education",
    "topup"
]


for category in categories:

    print("\n" + "=" * 50)
    print(f"CATEGORY: {category.upper()}")
    print("=" * 50)

    category_df = df[
        df["label"] == category
    ]

    print(
        f"Jumlah data: {len(category_df)}"
    )

    print()

    for text in category_df["text"].head(50):

        print("-", text)