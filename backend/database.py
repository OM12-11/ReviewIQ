from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Database directory
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite database file
DB_PATH = DATA_DIR / "reviewiq.db"

# Database connection URL
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"


# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for database models
Base = declarative_base()


# Database dependency for FastAPI
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()