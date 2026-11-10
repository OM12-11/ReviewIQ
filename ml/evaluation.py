import pandas as pd
import os

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# ============================================================
# PHASE 6 — MODEL EVALUATION
# ============================================================

INPUT_FILE = "data/processed/validation_sentiment.csv"
OUTPUT_FILE = "data/processed/evaluation_results.csv"

print("\n========================================")
print("        PHASE 6 — EVALUATION")
print("========================================\n")


# ============================================================
# 1. LOAD VALIDATION DATA
# ============================================================

print("Loading validation dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}\n")


# ============================================================
# 2. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "sentiment",
    "predicted_sentiment"
]

missing = [
    col for col in required_columns
    if col not in df.columns
]

if missing:
    print("❌ Missing columns:")
    print(missing)

    print("\nAvailable columns:")
    print(df.columns.tolist())

    raise ValueError(
        "Required evaluation columns are missing."
    )


# ============================================================
# 3. REMOVE INVALID ROWS
# ============================================================

df = df.dropna(
    subset=[
        "sentiment",
        "predicted_sentiment"
    ]
)

print(f"Valid rows for evaluation: {len(df)}\n")


# ============================================================
# 4. EXTRACT TRUE + PREDICTED LABELS
# ============================================================

y_true = (
    df["sentiment"]
    .astype(str)
    .str.lower()
    .str.strip()
)

y_pred = (
    df["predicted_sentiment"]
    .astype(str)
    .str.lower()
    .str.strip()
)


# ============================================================
# 5. CALCULATE METRICS
# ============================================================

accuracy = accuracy_score(
    y_true,
    y_pred
)

precision = precision_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    average="weighted",
    zero_division=0
)


# ============================================================
# 6. DISPLAY RESULTS
# ============================================================

print("========================================")
print("           EVALUATION RESULTS")
print("========================================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\n========================================")
print("        CLASSIFICATION REPORT")
print("========================================\n")

print(
    classification_report(
        y_true,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# 7. CONFUSION MATRIX
# ============================================================

print("========================================")
print("          CONFUSION MATRIX")
print("========================================\n")

labels = sorted(
    list(
        set(y_true) | set(y_pred)
    )
)

cm = confusion_matrix(
    y_true,
    y_pred,
    labels=labels
)

print("Labels:")
print(labels)

print("\nMatrix:")
print(cm)


# ============================================================
# 8. SAVE EVALUATION RESULTS
# ============================================================

results = pd.DataFrame({
    "metric": [
        "accuracy",
        "precision",
        "recall",
        "f1_score"
    ],
    "value": [
        accuracy,
        precision,
        recall,
        f1
    ]
})

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

results.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n========================================")
print("✅ PHASE 6 EVALUATION COMPLETE!")
print("========================================")

print(f"\nSaved to: {OUTPUT_FILE}")