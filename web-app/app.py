"""Web app"""
import os
import requests
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "lego_database"

client = MongoClient(MONGO_URI)
database = client[DB_NAME]

latest_result = None

@app.route("/")
def index():
    """ fetch the latest ML result from MongoDB """
    latest_result = database["readings"].find_one(sort=[("_id", -1)])
    if latest_result:
        # convert _id to string for JSON/templating
        latest_result["_id"] = str(latest_result["_id"])
    return render_template("index.html", result=latest_result)

@app.post("/receive_result")
def receive_result():
    """ Receive Base64 image from front-end, forward to ML service, and return result as json."""
    global latest_result

    # get the image from the request
    data = request.get_json(force=True)
    image_base64 = data.get("image_base64")
    if not image_base64:
        return jsonify({"error": "No image provided"}), 400

    #forward image to the ML container ? (confused on how docker works)
    try:
        ml_response = requests.post(
            "http://localhost:5000/process",
            json={"image": image_base64},
            timeout=10
        ).json()
    except requests.RequestException as e:
        return jsonify({"error": "Could not reach ML service", "details": str(e)}), 500

    latest_result = database["readings"].find_one(sort=[("_id", -1)])
    if latest_result:
        latest_result["_id"] = str(latest_result["_id"])

    # return the ML result as JSON
    return jsonify(ml_response)


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
