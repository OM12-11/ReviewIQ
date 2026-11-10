import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


INPUT_PATH = "data/raw/reviews_raw.csv"

TRAIN_PATH = "data/processed/train.csv"
VAL_PATH = "data/processed/validation.csv"
TEST_PATH = "data/processed/test.csv"


print("Loading dataset...")

df = pd.read_csv(INPUT_PATH)

print(f"Original rows: {len(df)}")


# ============================================================
# CLEAN DATASET
# ============================================================

# Keep only required columns
df = df[
    [
        "product_id",
        "product_title",
        "rating",
        "summary",
        "review"
    ]
]


# Remove duplicate reviews
df = df.drop_duplicates()


# Remove rows with missing review text
df = df.dropna(subset=["review"])


# Remove rows with missing ratings
df = df.dropna(subset=["rating"])


# Keep only valid ratings from 1 to 5
df = df[df["rating"].between(1, 5)]


# Convert review text to string
df["review"] = df["review"].astype(str)


# Remove empty reviews
df = df[df["review"].str.strip() != ""]


# Shuffle dataset
df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


print(f"Rows after cleaning: {len(df)}")


# ============================================================
# GROUPED TRAIN / VALIDATION / TEST SPLIT
# ============================================================

# 80% TRAIN
# 20% TEMPORARY

gss = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_idx, temp_idx = next(
    gss.split(
        df,
        groups=df["product_id"]
    )
)

train_df = df.iloc[train_idx].copy()
temp_df = df.iloc[temp_idx].copy()


# 10% VALIDATION
# 10% TEST

gss_temp = GroupShuffleSplit(
    n_splits=1,
    test_size=0.50,
    random_state=42
)

val_idx, test_idx = next(
    gss_temp.split(
        temp_df,
        groups=temp_df["product_id"]
    )
)

val_df = temp_df.iloc[val_idx].copy()
test_df = temp_df.iloc[test_idx].copy()


# ============================================================
# SAVE DATASETS
# ============================================================

train_df.to_csv(
    TRAIN_PATH,
    index=False
)

val_df.to_csv(
    VAL_PATH,
    index=False
)

test_df.to_csv(
    TEST_PATH,
    index=False
)


# ============================================================
# RESULTS
# ============================================================

print("\nDataset preparation complete!")

print(f"Train:      {len(train_df)} rows")
print(f"Validation: {len(val_df)} rows")
print(f"Test:       {len(test_df)} rows")

print("\nFiles created:")
print(TRAIN_PATH)
print(VAL_PATH)
print(TEST_PATH)