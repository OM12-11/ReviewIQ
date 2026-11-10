from flask import Blueprint, jsonify
import pandas as pd
import os

results_bp = Blueprint("results", __name__)

RESULT_FILE = "data/processed/train_aggregated.csv"


@results_bp.route("/results", methods=["GET"])
def get_results():

    if not os.path.exists(RESULT_FILE): 
        return jsonify({
            "success": False,
            "message": "Results file not found"
        }), 404

    try:
        df = pd.read_csv(RESULT_FILE)

        return jsonify({
            "success": True,
            "total_rows": len(df),
            "results": df.to_dict(orient="records")
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500