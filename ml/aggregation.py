import pandas as pd
import os


# ==========================================
# PHASE 5 — ASPECT SENTIMENT AGGREGATION
# ==========================================

INPUT_FILE = "data/processed/train_sentiment.csv"
OUTPUT_FILE = "data/processed/train_aggregated.csv"


print("\n========== PHASE 5 AGGREGATION ==========\n")


# ------------------------------------------
# 1. LOAD DATA
# ------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded!")
print(f"Rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")


# ------------------------------------------
# 2. CHECK REQUIRED COLUMNS
# ------------------------------------------
required_columns = [
    "product_id",
    "aspect",
    "rating",
    "sentiment"
]

missing = [
    col for col in required_columns
    if col not in df.columns
]

if missing:
    print("\n❌ Missing columns:")
    print(missing)
    raise ValueError("Required columns are missing.")


# ------------------------------------------
# 3. REMOVE INVALID ROWS
# ------------------------------------------

df = df.dropna(
    subset=[
        "product_id",
        "aspect",
        "sentiment"
    ]
)

df["aspect"] = df["aspect"].astype(str).str.lower().str.strip()
df["predicted_sentiment"] = (
    df["sentiment"]
    .astype(str)
    .str.lower()
    .str.strip()
)


# ------------------------------------------
# 4. SENTIMENT COUNTS
# ------------------------------------------

sentiment_counts = (
    df.groupby(
        ["product_id", "aspect", "sentiment"]
    )
    .size()
    .reset_index(name="count")
)

# ------------------------------------------
# 5. TOTAL REVIEWS PER ASPECT
# ------------------------------------------

total_reviews = (
    df.groupby(
        ["product_id", "aspect"]
    )
    .size()
    .reset_index(name="total_reviews")
)


# ------------------------------------------
# 6. MERGE COUNTS
# ------------------------------------------

aggregated = sentiment_counts.merge(
    total_reviews,
    on=["product_id", "aspect"]
)


# ------------------------------------------
# 7. CALCULATE SENTIMENT %
# ------------------------------------------

aggregated["percentage"] = (
    aggregated["count"]
    / aggregated["total_reviews"]
    * 100
)


# ------------------------------------------
# 8. AVERAGE RATING
# ------------------------------------------

avg_rating = (
    df.groupby(
        ["product_id", "aspect"]
    )["rating"]
    .mean()
    .reset_index(name="average_rating")
)

aggregated = aggregated.merge(
    avg_rating,
    on=["product_id", "aspect"]
)



# ------------------------------------------
# 10. SAVE RESULT
# ------------------------------------------

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

aggregated.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------
# 11. DISPLAY RESULT
# ------------------------------------------

print("\n========== AGGREGATION COMPLETE ==========\n")

print(
    aggregated.head(20).to_string(index=False)
)

print(
    f"\nSaved to: {OUTPUT_FILE}"
)

print("\n✅ PHASE 5 AGGREGATION COMPLETE!")