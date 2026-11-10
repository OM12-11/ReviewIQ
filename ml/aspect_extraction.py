import pandas as pd
import re

# ==============================
# FILE PATHS
# ==============================

TRAIN_PATH = "data/processed/train_processed.csv"
VAL_PATH = "data/processed/validation_processed.csv"
TEST_PATH = "data/processed/test.csv"


# ==============================
# ASPECT DEFINITIONS
# ==============================

ASPECTS = {
    "battery": [
        "battery",
        "battery life",
        "charging",
        "charge",
        "charger"
    ],

    "camera": [
        "camera",
        "photo",
        "photos",
        "picture",
        "pictures",
        "video",
        "selfie"
    ],

    "display": [
        "display",
        "screen",
        "touchscreen",
        "resolution",
        "brightness",
        "colour",
        "color"
    ],

    "performance": [
        "performance",
        "speed",
        "fast",
        "slow",
        "processor",
        "lag",
        "lagging",
        "ram"
    ],

    "price": [
        "price",
        "cost",
        "value",
        "expensive",
        "cheap",
        "money"
    ],

    "build": [
        "build",
        "body",
        "design",
        "quality",
        "material",
        "durability",
        "durable"
    ]
}


# ==============================
# ASPECT EXTRACTION FUNCTION
# ==============================

def extract_aspects(review):
    """
    Detect product aspects mentioned in a review.
    """

    if pd.isna(review):
        return []

    review = str(review).lower()

    detected_aspects = []

    for aspect, keywords in ASPECTS.items():

        for keyword in keywords:

            # Match whole words
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, review):
                detected_aspects.append(aspect)
                break

    return detected_aspects


# ==============================
# LOAD DATA
# ==============================

print("Loading datasets...")

train = pd.read_csv(TRAIN_PATH)
validation = pd.read_csv(VAL_PATH)
test = pd.read_csv(TEST_PATH)


# ==============================
# SELECT REVIEW COLUMN
# ==============================

def get_review_column(df, dataset_name):
    """
    Use clean_review if available.
    Otherwise use the original review column.
    """

    if "clean_review" in df.columns:
        print(f"{dataset_name}: using clean_review")
        return df["clean_review"]

    elif "review" in df.columns:
        print(f"{dataset_name}: clean_review not found, using review")
        return df["review"]

    else:
        raise ValueError(
            f"{dataset_name} dataset does not contain "
            f"'clean_review' or 'review' column."
        )


# ==============================
# APPLY ASPECT EXTRACTION
# ==============================

print("Extracting aspects...")

train_reviews = get_review_column(train, "Train")
validation_reviews = get_review_column(validation, "Validation")
test_reviews = get_review_column(test, "Test")

train["aspects"] = train_reviews.apply(extract_aspects)
validation["aspects"] = validation_reviews.apply(extract_aspects)
test["aspects"] = test_reviews.apply(extract_aspects)

# ==============================
# CONVERT LIST TO STRING
# ==============================

train["aspects"] = train["aspects"].apply(lambda x: "|".join(x))
validation["aspects"] = validation["aspects"].apply(lambda x: "|".join(x))
test["aspects"] = test["aspects"].apply(lambda x: "|".join(x))


# ==============================
# SAVE RESULTS
# ==============================

train.to_csv("data/processed/train_aspects.csv", index=False)
validation.to_csv("data/processed/validation_aspects.csv", index=False)
test.to_csv("data/processed/test_aspects.csv", index=False)


# ==============================
# SHOW RESULTS
# ==============================

print("\n==============================")
print("PHASE 3 ASPECT EXTRACTION")
print("==============================")

print("Train rows:", len(train))
print("Validation rows:", len(validation))
print("Test rows:", len(test))

print("\nExample extracted aspects:")

for i in range(min(10, len(train))):
    print("\nReview:", train.iloc[i]["clean_review"])
    print("Aspects:", train.iloc[i]["aspects"])

print("\n==============================")
print("PHASE 3 EXTRACTION COMPLETE!")
print("==============================")