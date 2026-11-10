from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.sql import func

from backend.database import Base


# Main customer reviews table
class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(String, nullable=False, index=True)

    product_title = Column(String, nullable=True)

    rating = Column(Float, nullable=False)

    review = Column(Text, nullable=False)

    aspect = Column(String, nullable=True)

    sentiment = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Aspect-level sentiment analysis results
class ReviewAspect(Base):

    __tablename__ = "review_aspects"

    id = Column(Integer, primary_key=True, index=True)

    review_id = Column(
        Integer,
        ForeignKey("reviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    aspect = Column(String, nullable=False)

    sentiment = Column(String, nullable=False)

    confidence = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "review_id",
            "aspect",
            name="unique_review_aspect"
        ),
    )