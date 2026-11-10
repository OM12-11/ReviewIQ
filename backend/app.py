from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

from routes.analysis import analysis_bp
from routes.results import results_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(analysis_bp, url_prefix="/api")
app.register_blueprint(results_bp, url_prefix="/api")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AGGREGATED_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "train_aggregated.csv"
)

EVALUATION_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "evaluation_results.csv"
)


@app.route("/")
def home():
    return jsonify({
        "message": "Review IQ API is running",
        "status": "success"
    })


@app.route("/api/summary")
def summary():

    if not os.path.exists(AGGREGATED_FILE):
        return jsonify({
            "error": "Aggregated dataset not found"
        }), 404

    df = pd.read_csv(AGGREGATED_FILE)

    return jsonify({
        "total_records": len(df),
        "total_products": int(df["product_id"].nunique()),
        "total_aspects": int(df["aspect"].nunique()),
        "average_rating": round(float(df["average_rating"].mean()), 2)
    })


@app.route("/api/aspects")
def aspects():

    if not os.path.exists(AGGREGATED_FILE):
        return jsonify({
            "error": "Aggregated dataset not found"
        }), 404

    df = pd.read_csv(AGGREGATED_FILE)

    result = df.to_dict(orient="records")

    return jsonify(result)


@app.route("/api/evaluation")
def evaluation():

    if not os.path.exists(EVALUATION_FILE):
        return jsonify({
            "error": "Evaluation results not found"
        }), 404

    df = pd.read_csv(EVALUATION_FILE)

    return jsonify(
        df.to_dict(orient="records")
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )

@app.route("/api/reviews", methods=["GET"])
def reviews():
    import pandas as pd

    file_path = "data/processed/train_aggregated.csv"

    df = pd.read_csv(file_path)

    records = df.to_dict(orient="records")

    return jsonify(records)