import pandas as pd

DATASET_PATH = "data/raw/reviews_raw.csv"

df = pd.read_csv(DATASET_PATH)

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== COLUMNS =====")
print(df.columns.tolist())

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATES =====")
print("Duplicate rows:", df.duplicated().sum())

print("\n===== RATING DISTRIBUTION =====")
if "rating" in df.columns:
    print(df["rating"].value_counts().sort_index())