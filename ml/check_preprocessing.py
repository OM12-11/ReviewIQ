import pandas as pd


FILES = {
    "Train": "data/processed/train_processed.csv",
    "Validation": "data/processed/validation_processed.csv",
    "Test": "data/processed/test_processed.csv",
}


print("\n========== PHASE 2 CHECK ==========")


all_passed = True


for name, path in FILES.items():

    df = pd.read_csv(path)

    print(f"\n{name}")
    print("-" * 30)

    print("Rows:", len(df))

    print("Missing reviews:",
          df["clean_review"].isnull().sum())

    print("Empty reviews:",
          (df["clean_review"].astype(str).str.strip() == "").sum())

    print("Missing ratings:",
          df["rating"].isnull().sum())

    print("Columns:")
    print(list(df.columns))

    # Checks
    if df["clean_review"].isnull().sum() != 0:
        all_passed = False

    if (df["clean_review"].astype(str).str.strip() == "").sum() != 0:
        all_passed = False

    if df["rating"].isnull().sum() != 0:
        all_passed = False


print("\n========== FINAL RESULT ==========")

if all_passed:
    print("✅ PHASE 2 PREPROCESSING PASSED!")
    print("🎉 NLP preprocessing is ready for the next phase.")
else:
    print("⚠️ PHASE 2 NEEDS ATTENTION!")