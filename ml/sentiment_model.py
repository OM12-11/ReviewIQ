import pandas as pd
import numpy as np
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# CONFIGURATION
# ============================================================

TRAIN_PATH = "data/processed/train_aspects.csv"
VAL_PATH = "data/processed/validation_aspects.csv"
TEST_PATH = "data/processed/test_processed.csv"

OUTPUT_DIR = "data/processed"
MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "sentiment_pipeline.joblib"
)

# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("PHASE 4 — SENTIMENT ANALYSIS")
print("=" * 60)

print("\nLoading datasets...")

train = pd.read_csv(TRAIN_PATH)
val = pd.read_csv(VAL_PATH)

print(f"Train rows: {len(train)}")
print(f"Validation rows: {len(val)}")


# ============================================================
# CREATE SENTIMENT LABEL FROM RATING
# ============================================================

def rating_to_sentiment(rating):
    """
    Convert star rating into sentiment.

    1-2 -> Negative
    3   -> Neutral
    4-5 -> Positive
    """

    if pd.isna(rating):
        return None

    rating = float(rating)

    if rating <= 2:
        return "negative"

    elif rating == 3:
        return "neutral"

    else:
        return "positive"


train["sentiment"] = train["rating"].apply(rating_to_sentiment)
val["sentiment"] = val["rating"].apply(rating_to_sentiment)


# ============================================================
# EXPAND ASPECTS
# ============================================================

def expand_aspects(df):
    """
    Convert:

        aspects = battery|price|build

    into separate rows:

        battery
        price
        build
    """

    rows = []

    for _, row in df.iterrows():

        aspects = row["aspects"]

        # Ignore missing aspects
        if pd.isna(aspects):
            continue

        aspects = str(aspects).strip()

        if not aspects:
            continue

        # Split multiple aspects
        aspect_list = [
            aspect.strip()
            for aspect in aspects.split("|")
            if aspect.strip()
        ]

        for aspect in aspect_list:

            rows.append({
                "product_id": row["product_id"],
                "product_title": row["product_title"],
                "rating": row["rating"],
                "review": row["review"],
                "clean_review": row["clean_review"],
                "aspect": aspect,
                "sentiment": row["sentiment"]
            })

    return pd.DataFrame(rows)


print("\nExpanding aspects...")

train_expanded = expand_aspects(train)
val_expanded = expand_aspects(val)

print(f"Train aspect samples: {len(train_expanded)}")
print(f"Validation aspect samples: {len(val_expanded)}")


# ============================================================
# REMOVE INVALID ROWS
# ============================================================

train_expanded = train_expanded.dropna(
    subset=["clean_review", "aspect", "sentiment"]
)

val_expanded = val_expanded.dropna(
    subset=["clean_review", "aspect", "sentiment"]
)

train_expanded = train_expanded[
    train_expanded["clean_review"].astype(str).str.strip() != ""
]

val_expanded = val_expanded[
    val_expanded["clean_review"].astype(str).str.strip() != ""
]


# ============================================================
# CREATE MODEL INPUT
# ============================================================

print("\nCreating aspect-aware text...")

train_expanded["model_text"] = (
    "aspect: "
    + train_expanded["aspect"].astype(str)
    + " review: "
    + train_expanded["clean_review"].astype(str)
)

val_expanded["model_text"] = (
    "aspect: "
    + val_expanded["aspect"].astype(str)
    + " review: "
    + val_expanded["clean_review"].astype(str)
)


X_train = train_expanded["model_text"]
y_train = train_expanded["sentiment"]

X_val = val_expanded["model_text"]
y_val = val_expanded["sentiment"]


# ============================================================
# CHECK SENTIMENT DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("SENTIMENT DISTRIBUTION")
print("=" * 60)

print("\nTrain:")
print(y_train.value_counts())

print("\nValidation:")
print(y_val.value_counts())


# ============================================================
# BUILD TF-IDF + LOGISTIC REGRESSION MODEL
# ============================================================

print("\n" + "=" * 60)
print("TRAINING SENTIMENT MODEL")
print("=" * 60)

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
            sublinear_tf=True
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )
])


print("\nTraining...")

model.fit(X_train, y_train)

print("Training complete!")

# Save the complete ML pipeline
joblib.dump(model, MODEL_PATH)

print(f"Model saved successfully: {MODEL_PATH}")
# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("VALIDATION RESULTS")
print("=" * 60)

y_pred = model.predict(X_val)

accuracy = accuracy_score(y_val, y_pred)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_val,
        y_pred,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_val,
        y_pred
    )
)


# ============================================================
# PREDICTIONS + CONFIDENCE
# ============================================================

print("\nGenerating predictions...")

val_expanded["predicted_sentiment"] = y_pred

probabilities = model.predict_proba(X_val)

val_expanded["confidence"] = probabilities.max(axis=1)


# ============================================================
# SAVE RESULTS
# ============================================================

output_path = os.path.join(
    OUTPUT_DIR,
    "validation_sentiment.csv"
)

val_expanded.to_csv(
    output_path,
    index=False
)


# ============================================================
# SAVE TRAINING DATA
# ============================================================

train_output_path = os.path.join(
    OUTPUT_DIR,
    "train_sentiment.csv"
)

train_expanded.to_csv(
    train_output_path,
    index=False
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 60)
print("PHASE 4 RESULT")
print("=" * 60)

print("✅ Sentiment model trained successfully!")
print(f"✅ Validation accuracy: {accuracy:.4f}")

print("\nFiles created:")

print(f"  {train_output_path}")
print(f"  {output_path}")

print("\nSample predictions:")

print(
    val_expanded[
        [
            "aspect",
            "rating",
            "predicted_sentiment",
            "confidence"
        ]
    ].head(10).to_string(index=False)
)

print("\n🎉 PHASE 4 SENTIMENT ANALYSIS COMPLETE!")