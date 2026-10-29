from fastapi import FastAPI

app = FastAPI(
    title="ReviewIQ API",
    description="Intelligent Product Feedback Analysis using NLP",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "ReviewIQ API is running!"
    }