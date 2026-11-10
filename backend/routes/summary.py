from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models import Review, ReviewAspect


router = APIRouter()


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):

    # Total uploaded reviews
    total_reviews = db.query(Review).count()

    # Total aspect predictions
    total_predictions = db.query(ReviewAspect).count()

    # Number of unique reviews analyzed
    analyzed_reviews = db.query(
        func.count(func.distinct(ReviewAspect.review_id))
    ).scalar() or 0

    # Reviews without aspect predictions
    unanalyzed_reviews = total_reviews - analyzed_reviews

    # Sentiment counts
    sentiment_data = db.query(
        ReviewAspect.sentiment,
        func.count(ReviewAspect.id)
    ).group_by(
        ReviewAspect.sentiment
    ).all()

    sentiment_counts = {
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }

    for sentiment, count in sentiment_data:
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] = count

    # Calculate sentiment percentages
    sentiment_distribution = {}

    for sentiment, count in sentiment_counts.items():

        percentage = (
            (count / total_predictions) * 100
            if total_predictions > 0 else 0
        )

        sentiment_distribution[sentiment] = {
            "count": count,
            "percentage": round(percentage, 2)
        }

    # Average prediction confidence
    average_confidence = db.query(
        func.avg(ReviewAspect.confidence)
    ).scalar()

    # Aspect-wise prediction counts
    aspect_data = db.query(
        ReviewAspect.aspect,
        func.count(ReviewAspect.id)
    ).group_by(
        ReviewAspect.aspect
    ).all()

    aspect_distribution = {
        aspect: count
        for aspect, count in aspect_data
    }

    # Total products
    total_products = db.query(
        func.count(func.distinct(Review.product_id))
    ).scalar() or 0

    return {
        "success": True,
        "dashboard_summary": {
            "total_reviews": total_reviews,
            "analyzed_reviews": analyzed_reviews,
            "unanalyzed_reviews": unanalyzed_reviews,
            "total_predictions": total_predictions,
            "total_products": total_products,
            "sentiment_distribution": sentiment_distribution,
            "average_confidence": round(
                float(average_confidence), 4
            ) if average_confidence is not None else None,
            "aspect_distribution": aspect_distribution
        }
    }
@router.get("/summary/aspects")
def get_aspect_analysis(db: Session = Depends(get_db)):

    results = db.query(
        ReviewAspect.aspect,
        ReviewAspect.sentiment,
        func.count(ReviewAspect.id)
    ).group_by(
        ReviewAspect.aspect,
        ReviewAspect.sentiment
    ).all()

    aspect_analysis = {}

    for aspect, sentiment, count in results:

        if aspect not in aspect_analysis:
            aspect_analysis[aspect] = {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }

        if sentiment in aspect_analysis[aspect]:
            aspect_analysis[aspect][sentiment] = count

    return {
        "success": True,
        "aspect_analysis": aspect_analysis
    }


@router.get("/summary/products")
def get_product_analysis(db: Session = Depends(get_db)):

    # 1. Get total reviews for each product
    product_rows = db.query(
        Review.product_id,
        func.max(Review.product_title),
        func.count(Review.id)
    ).group_by(
        Review.product_id
    ).all()

    # 2. Get sentiment counts for each product
    sentiment_rows = db.query(
        Review.product_id,
        ReviewAspect.sentiment,
        func.count(ReviewAspect.id)
    ).join(
        ReviewAspect,
        Review.id == ReviewAspect.review_id
    ).group_by(
        Review.product_id,
        ReviewAspect.sentiment
    ).all()

    # 3. Get unique analyzed review counts per product
    analyzed_rows = db.query(
        Review.product_id,
        func.count(func.distinct(ReviewAspect.review_id))
    ).join(
        ReviewAspect,
        Review.id == ReviewAspect.review_id
    ).group_by(
        Review.product_id
    ).all()

    # 4. Prepare product-wise response
    products = {}

    for product_id, product_title, total_reviews in product_rows:

        products[product_id] = {
            "product_id": product_id,
            "product_title": product_title,
            "total_reviews": total_reviews,
            "analyzed_reviews": 0,
            "total_predictions": 0,
            "sentiment_distribution": {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }
        }

    # 5. Add sentiment counts
    for product_id, sentiment, count in sentiment_rows:

        if product_id in products:
            products[product_id]["sentiment_distribution"][sentiment] = count
            products[product_id]["total_predictions"] += count

    # 6. Add analyzed review counts
    for product_id, count in analyzed_rows:

        if product_id in products:
            products[product_id]["analyzed_reviews"] = count

    # 7. Calculate sentiment percentages and dominant sentiment
    for product in products.values():

        total = product["total_predictions"]

        distribution = product["sentiment_distribution"]

        if total > 0:

            product["sentiment_percentages"] = {
                sentiment: round((count / total) * 100, 2)
                for sentiment, count in distribution.items()
            }

            product["dominant_sentiment"] = max(
                distribution,
                key=distribution.get
            )

        else:

            product["sentiment_percentages"] = {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }

            product["dominant_sentiment"] = None

    return {
        "success": True,
        "total_products": len(products),
        "product_analysis": list(products.values())
    }
