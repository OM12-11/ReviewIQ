import pandas as pd

TRAIN_PATH = "data/processed/train.csv"
VAL_PATH = "data/processed/validation.csv"
TEST_PATH = "data/processed/test.csv"


print("========== LOADING DATASETS ==========")

train = pd.read_csv(TRAIN_PATH)
val = pd.read_csv(VAL_PATH)
test = pd.read_csv(TEST_PATH)


# --------------------------------------------------
# 1. Check dataset sizes
# --------------------------------------------------

print("\n========== DATASET SIZES ==========")

print("Train:", len(train))
print("Validation:", len(val))
print("Test:", len(test))
print("Total:", len(train) + len(val) + len(test))


# --------------------------------------------------
# 2. Check missing values
# --------------------------------------------------

print("\n========== MISSING VALUES ==========")

print("Train:")
print(train.isnull().sum())

print("\nValidation:")
print(val.isnull().sum())

print("\nTest:")
print(test.isnull().sum())


# --------------------------------------------------
# 3. Check ratings
# --------------------------------------------------

print("\n========== RATING CHECK ==========")

print("Train ratings:")
print(train["rating"].value_counts().sort_index())

print("\nValidation ratings:")
print(val["rating"].value_counts().sort_index())

print("\nTest ratings:")
print(test["rating"].value_counts().sort_index())


# --------------------------------------------------
# 4. Check invalid ratings
# --------------------------------------------------

print("\n========== INVALID RATINGS ==========")

for name, df in [
    ("Train", train),
    ("Validation", val),
    ("Test", test)
]:
    invalid = df[~df["rating"].isin([1, 2, 3, 4, 5])]

    print(f"{name}: {len(invalid)} invalid ratings")


# --------------------------------------------------
# 5. Check empty reviews
# --------------------------------------------------

print("\n========== EMPTY REVIEWS ==========")

for name, df in [
    ("Train", train),
    ("Validation", val),
    ("Test", test)
]:
    empty = df["review"].astype(str).str.strip().eq("").sum()

    print(f"{name}: {empty} empty reviews")


# --------------------------------------------------
# 6. Check duplicates inside each dataset
# --------------------------------------------------

print("\n========== DUPLICATES ==========")

print("Train duplicates:", train.duplicated().sum())
print("Validation duplicates:", val.duplicated().sum())
print("Test duplicates:", test.duplicated().sum())


# --------------------------------------------------
# 7. Check overlap between datasets
# --------------------------------------------------

print("\n========== DATASET OVERLAP ==========")

train_products = set(train["product_id"])
val_products = set(val["product_id"])
test_products = set(test["product_id"])

train_val_overlap = train_products & val_products
train_test_overlap = train_products & test_products
val_test_overlap = val_products & test_products

print("Train ↔ Validation:", len(train_val_overlap))
print("Train ↔ Test:", len(train_test_overlap))
print("Validation ↔ Test:", len(val_test_overlap))

print("\n========== REVIEW TEXT OVERLAP ==========")

train_reviews = set(train["review"])
val_reviews = set(val["review"])
test_reviews = set(test["review"])

print("Train ↔ Validation:", len(train_reviews & val_reviews))
print("Train ↔ Test:", len(train_reviews & test_reviews))
print("Validation ↔ Test:", len(val_reviews & test_reviews))

# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

print("\n========== FINAL RESULT ==========")

if (
    train.isnull()["review"].sum() == 0
    and val.isnull()["review"].sum() == 0
    and test.isnull()["review"].sum() == 0
    and train["rating"].isin([1, 2, 3, 4, 5]).all()
    and val["rating"].isin([1, 2, 3, 4, 5]).all()
    and test["rating"].isin([1, 2, 3, 4, 5]).all()
    and train.duplicated().sum() == 0
    and val.duplicated().sum() == 0
    and test.duplicated().sum() == 0
    and len(train_products & val_products) == 0
    and len(train_products & test_products) == 0
    and len(val_products & test_products) == 0):
    print("✅ DATASET PASSED ALL CHECKS!")
    print("🎉 Phase 1 is officially complete!")

else:
    print("⚠️ DATASET NEEDS ATTENTION")