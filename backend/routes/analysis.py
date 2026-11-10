from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.models import Review, ReviewAspect

from pathlib import Path
import pandas as pd
import joblib
import re


router = APIRouter()

# Model path
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "sentiment_pipeline.joblib"

# Load model once when API module loads
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Sentiment model not found: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)


# Aspect keywords
ASPECTS = {
    "battery": [
        "battery", "battery life", "charging", "charge", "charger"
    ],
    "camera": [
        "camera", "photo", "photos", "picture", "pictures",
        "video", "selfie"
    ],
    "display": [
        "display", "screen", "touchscreen", "resolution",
        "brightness", "colour", "color"
    ],
    "performance": [
        "performance", "speed", "fast", "slow",
        "processor", "lag", "lagging", "ram"
    ],
    "price": [
        "price", "cost", "value", "expensive", "cheap", "money"
    ],
    "build": [
        "build", "body", "design", "quality",
        "material", "durability", "durable"
    ]
}


# Text cleaning
def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    text = re.sub(r"<[^>]+>", " ", text)

    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# Extract aspects
def extract_aspects(review):

    if pd.isna(review):
        return []

    review = str(review).lower()

    detected_aspects = []

    for aspect, keywords in ASPECTS.items():

        for keyword in keywords:

            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, review):
                detected_aspects.append(aspect)
                break

    return detected_aspects


# Analyze all reviews
@router.post("/analyze")
def analyze_reviews(db: Session = Depends(get_db)):

    try:

        reviews = db.query(Review).all()

        if not reviews:
            raise HTTPException(
                status_code=404,
                detail="No reviews found. Upload a dataset first."
            )

        saved_count = 0
        skipped_count = 0

        for review in reviews:

            cleaned_review = clean_text(review.review)

            aspects = extract_aspects(cleaned_review)

            for aspect in aspects:

                # Avoid duplicate aspect predictions
                existing = db.query(ReviewAspect).filter_by(
                    review_id=review.id,
                    aspect=aspect
                ).first()

                if existing:
                    skipped_count += 1
                    continue

                model_input = (
                    f"aspect: {aspect} review: {cleaned_review}"
                )

                prediction = model.predict([model_input])[0]

                probabilities = model.predict_proba([model_input])[0]

                confidence = float(max(probabilities))

                result = ReviewAspect(
                    review_id=review.id,
                    aspect=aspect,
                    sentiment=str(prediction),
                    confidence=confidence
                )

                db.add(result)

                saved_count += 1

        db.commit()

        total_results = db.query(ReviewAspect).count()

        return {
            "success": True,
            "message": "Aspect-level sentiment analysis completed",
            "total_reviews": len(reviews),
            "new_predictions_saved": saved_count,
            "existing_predictions_skipped": skipped_count,
            "total_predictions_in_database": total_results
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Get analysis results
@router.get("/analysis/results")
def get_analysis_results(db: Session = Depends(get_db)):

    results = db.query(ReviewAspect).all()

    return [
        {
            "review_id": result.review_id,
            "aspect": result.aspect,
            "sentiment": result.sentiment,
            "confidence": result.confidence
        }
        for result in results
    ]