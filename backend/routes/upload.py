
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from pathlib import Path
from io import BytesIO
import pandas as pd
import uuid
import math

from backend.database import get_db
from backend.models import Review


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    filename_original = file.filename or ""

    # 1. Validate file extension
    if not filename_original.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported"
        )

    try:

        # 2. Read CSV
        contents = await file.read()

        df = pd.read_csv(BytesIO(contents))

        required_columns = [
            "product_id",
            "product_title",
            "rating",
            "review"
        ]

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid dataset",
                    "missing_columns": missing_columns
                }
            )

        # 3. Retrieve existing reviews
        existing_reviews = db.query(
            Review.product_id,
            Review.product_title,
            Review.rating,
            Review.review
        ).all()

        # Create a set of existing review fingerprints
        existing_keys = set()

        for record in existing_reviews:

            key = (
                str(record.product_id).strip(),
                record.product_title.strip()
                if record.product_title else None,
                float(record.rating),
                str(record.review).strip()
            )

            existing_keys.add(key)

        # 4. Process uploaded records
        new_records = []

        duplicate_count = 0
        invalid_count = 0

        for _, row in df.iterrows():

            # Validate required values
            if (
                pd.isna(row["product_id"])
                or pd.isna(row["rating"])
                or pd.isna(row["review"])
            ):
                invalid_count += 1
                continue

            product_id = str(row["product_id"]).strip()

            product_title = (
                str(row["product_title"]).strip()
                if pd.notna(row["product_title"])
                else None
            )

            review_text = str(row["review"]).strip()

            try:
                rating = float(row["rating"])
            except (ValueError, TypeError):
                invalid_count += 1
                continue

            # Validate rating and review
            if (
                not product_id
                or not review_text
                or not math.isfinite(rating)
                or rating < 1
                or rating > 5
            ):
                invalid_count += 1
                continue

            # 5. Generate unique review fingerprint
            review_key = (
                product_id,
                product_title,
                rating,
                review_text
            )

            # Check existing database and current CSV
            if review_key in existing_keys:
                duplicate_count += 1
                continue

            # 6. Create new database record
            record = Review(
                product_id=product_id,
                product_title=product_title,
                rating=rating,
                review=review_text,
                aspect=None,
                sentiment=None
            )

            new_records.append(record)

            # Prevent duplicates within the same CSV
            existing_keys.add(review_key)

        # 7. Save uploaded CSV
        file_id = str(uuid.uuid4())
        saved_filename = f"{file_id}.csv"
        file_path = UPLOAD_DIR / saved_filename

        with open(file_path, "wb") as f:
            f.write(contents)

        # 8. Insert only new records
        db.add_all(new_records)
        db.commit()

        return {
            "success": True,
            "message": "Dataset processed successfully",

            "file_id": file_id,
            "filename": saved_filename,

            "total_rows": len(df),
            "records_saved": len(new_records),
            "records_duplicate": duplicate_count,
            "records_invalid": invalid_count,

            "records_skipped": duplicate_count + invalid_count
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
