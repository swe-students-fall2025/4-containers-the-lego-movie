"""
Web app entrypoint.
"""
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = "lego_database"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

@app.route("/")
def index():
    results = list(db["analysis_results"].find().sort("_id", -1).limit(10))
    return render_template("index.html", results=results)

@app.route("/api/results")
def api_results():
    results = list(db["analysis_results"].find().sort("_id", -1).limit(10))
    for r in results:
        r["_id"] = str(r["_id"])
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
