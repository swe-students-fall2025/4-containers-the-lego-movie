"""
Web app entrypoint.
"""

# import os 

from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "lego_database"

client = MongoClient(MONGO_URI)
database = client[DB_NAME]


@app.route("/")
def index():
    """Render the home page with the latest analysis results."""
    analysis_results = list(
        database["analysis_results"].find().sort("_id", -1).limit(10)
    )
    return render_template("index.html", results=analysis_results)


@app.route("/api/results")
def api_results():
    """Return the latest analysis results as JSON."""
    analysis_results = list(
        database["analysis_results"].find().sort("_id", -1).limit(10)
    )
    for analysis_result in analysis_results:
        analysis_result["_id"] = str(analysis_result["_id"])
    return jsonify(analysis_results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
