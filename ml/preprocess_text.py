import pandas as pd
import re
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

INPUT_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/processed")


FILES = {
    "train": INPUT_DIR / "train.csv",
    "validation": INPUT_DIR / "validation.csv",
    "test": INPUT_DIR / "test.csv",
}


# ============================================================
# TEXT CLEANING FUNCTION
# ============================================================

def clean_text(text):
    """
    Clean review text while preserving useful
    sentiment information for transformer models.
    """

    if pd.isna(text):
        return ""

    text = str(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # Normalize repeated whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text


# ============================================================
# PROCESS EACH DATASET
# ============================================================

for name, path in FILES.items():

    print(f"\nLoading {name} dataset...")
    
    df = pd.read_csv(path)

    print(f"Original rows: {len(df)}")

    # Clean review text
    df["review"] = df["review"].apply(clean_text)

    # Remove rows where review became empty
    df = df[df["review"].str.strip() != ""]

    # Create a clean text column
    df["clean_review"] = df["review"]

    # Save processed dataset
    output_path = OUTPUT_DIR / f"{name}_processed.csv"

    df.to_csv(output_path, index=False)

    print(f"Processed rows: {len(df)}")
    print(f"Saved to: {output_path}")


print("\n================================")
print("PHASE 2 TEXT PREPROCESSING DONE!")
print("================================")