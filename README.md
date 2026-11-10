# ReviewIQ - Product Review Intelligence Dashboard

ReviewIQ is an NLP-powered product review analysis system that helps users understand customer feedback through sentiment classification, aspect extraction, and interactive visualizations.

The application allows users to upload product review datasets, analyze customer opinions, and explore product-level and aspect-level feedback through a dashboard.

## Key Features

- Upload product review datasets in CSV format.
- Validate uploaded datasets.
- Preprocess customer review text.
- Extract product aspects using keyword-based extraction.
- Classify sentiment into Positive, Negative, and Neutral.
- Aggregate sentiment results by product and aspect.
- Identify frequently discussed product aspects.
- Explore analysis results through interactive charts.
- Store reviews and analysis data using SQLite.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Text Vectorization | TF-IDF |
| Classification Algorithm | Logistic Regression |
| Database | SQLite |
| ORM | SQLAlchemy |
| Data Visualization | Chart.js |
| API Documentation | Swagger UI |

## Machine Learning Approach

ReviewIQ uses a machine learning pipeline consisting of:

1. Text preprocessing.
2. Keyword-based product aspect extraction.
3. TF-IDF text vectorization.
4. Logistic Regression sentiment classification.
5. Product and aspect-level sentiment aggregation.

### Sentiment Classes

The model predicts three sentiment categories:

- Positive
- Negative
- Neutral

### Aspect Extraction

The current aspect extraction component identifies six product aspects:

- Battery
- Camera
- Display
- Performance
- Price
- Build Quality

### Model Input

The model receives text containing both the extracted aspect and the cleaned review.

Example:

`aspect: battery review: battery life is excellent`

The trained model is stored at:

`models/sentiment_pipeline.joblib`

**Important:** The current training pipeline derives sentiment labels from overall review ratings:

- Ratings 1–2 → Negative
- Rating 3 → Neutral
- Ratings 4–5 → Positive

These labels are transferred to extracted aspect records. Therefore, aspect-level sentiment is currently an approximation based on the overall review rating, not independently human-annotated aspect sentiment.

## Project Structure

```text
ReviewIQ/
│
├── backend/
│   ├── main.py
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   └── routes/
│       ├── analysis.py
│       ├── product.py
│       ├── results.py
│       ├── reviews.py
│       ├── summary.py
│       └── upload.py
│
├── database/
│   └── schema.sql
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── test/
│   ├── uploads/
│   └── reviewiq.db
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js
│       ├── app.js
│       ├── charts.js
│       └── dashboard.js
│
├── ml/
│   ├── aggregation.py
│   ├── aspect_extraction.py
│   ├── check_dataset.py
│   ├── check_preprocessing.py
│   ├── evaluation.py
│   ├── inspect_dataset.py
│   ├── prepare_dataset.py
│   ├── preprocess_text.py
│   ├── preprocessing.py
│   └── sentiment_model.py
│
├── models/
│   └── sentiment_pipeline.joblib
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### Prerequisites

Install the following:

- Python 3.10 or later
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/OM12-11/ReviewIQ.git
```

Navigate into the project:

```bash
cd ReviewIQ
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

ReviewIQ has two components: the FastAPI backend and the frontend dashboard.

Both must run simultaneously.

### 1. Start the Backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

Swagger API documentation:

`http://127.0.0.1:8000/docs`

### 2. Start the Frontend

Open a second terminal.

Navigate to the frontend directory:

```bash
cd frontend
```

Start the frontend server:

```bash
python -m http.server 5500
```

Open the dashboard:

`http://127.0.0.1:5500`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/upload` | Upload a review CSV |
| POST | `/api/analyze` | Analyze uploaded reviews |
| GET | `/api/analysis/results` | Retrieve analysis results |
| GET | `/api/summary` | Retrieve overall summary |
| GET | `/api/summary/aspects` | Retrieve aspect-level summary |
| GET | `/api/summary/products` | Retrieve product-level summary |

Interactive API documentation is available through Swagger UI at `/docs`.

## CSV Upload Format

Uploaded CSV files must contain these columns:

| Column | Description |
|---|---|
| `product_id` | Unique product identifier |
| `product_title` | Product name |
| `rating` | Customer rating from 1 to 5 |
| `review` | Customer review text |

Example:

```csv
product_id,product_title,rating,review
101,Smartphone,5,Excellent camera and battery life
102,Laptop,2,Very poor performance
103,Wireless Earbuds,4,Good sound quality
```

The application validates the uploaded CSV structure and rating values before processing.

## Database

ReviewIQ currently uses SQLite with SQLAlchemy.

The local database is stored at:

`data/reviewiq.db`

The repository includes a database snapshot containing existing project data.

## Model Artifact

The trained sentiment classification pipeline is stored at:

`models/sentiment_pipeline.joblib`

The application loads this saved model for sentiment prediction rather than requiring model training every time it starts.

## Current Project Status

Implemented:

- FastAPI backend.
- SQLite database integration.
- CSV upload and validation.
- Text preprocessing.
- Keyword-based aspect extraction.
- Sentiment classification.
- Product and aspect-level aggregation.
- Interactive frontend dashboard.
- API documentation using Swagger UI.
- Saved machine learning pipeline.

## Future Improvements

- Fine-grained aspect-level sentiment annotation.
- Transformer-based sentiment classification.
- Improved aspect extraction using NLP models.
- Production database deployment.
- Cloud hosting and public application access.
- Authentication and user management.
- Automated model retraining.

## Running Locally vs. Cloud Deployment

The current repository provides a locally runnable application.

Running the application locally does not automatically make the dashboard publicly accessible. Cloud deployment, production database configuration, persistent file storage, and production CORS configuration are separate future steps.

## Author

Developed as an applied Machine Learning and NLP project.