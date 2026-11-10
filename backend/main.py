from fastapi import FastAPI
from backend.database import engine, Base
from backend import models
from backend.routes.upload import router as upload_router
from backend.routes.analysis import router as analysis_router
from backend.routes.summary import router as summary_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ReviewIQ API",
    description="Intelligent Product Feedback Analysis using NLP",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)
app.include_router(
    upload_router,
    prefix="/api",
    tags=["Upload"]
)
app.include_router(
    analysis_router,
    prefix="/api",
    tags=["Analysis"]
)
app.include_router(
    summary_router,
    prefix="/api",
    tags=["Dashboard"]
)


@app.get("/")
def root():
    return {
        "message": "ReviewIQ API is running!",
        "database": "SQLite connected"
    }