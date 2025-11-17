"""Machine learning client that simulates sensor readings and stores them in MongoDB."""

import base64
import time
import random
from datetime import datetime, timezone
from io import BytesIO

from pymongo import MongoClient
from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)


def collect_data():
    """Simulate collecting a sensor reading.

    Returns a dictionary with a random float value and a UTC timestamp.
    """
    return {
        "value": random.random(),
        "timestamp": datetime.now(timezone.utc),
    }


def analyze_image(image_base64: str):
    """Classify a numeric value as either 'high' or 'low'.

    Values greater than 0.5 are classified as 'high', all others as 'low'.
    """
    img_bytes = base64.b64decode(image_base64)
    img = Image.open(BytesIO(img_bytes))
    gray = img.convert("L")
    pixels = list(gray.getdata())
    avg = sum(pixels) / len(pixels)

    return "high" if avg > 128 else "low"


def save_to_db(collection, image_base64, analysis):
    """Stores metadata about the received image + analysis result."""
    document = {
        "analysis": analysis,
        "timestamp": datetime.now(timezone.utc),
        "image_length": len(image_base64),
    }
    result = collection.insert_one(document)
    return result.inserted_id


def get_db():
    client = MongoClient("mongodb://mongodb:27017")
    return client["ml_db"]


def process_incoming_image(image_base64: str):
    """Called by web-app to process a frame."""
    analysis = analyze_image(image_base64)

    db = get_db()
    readings = db["readings"]

    inserted_id = save_to_db(readings, image_base64, analysis)
    return {"id": str(inserted_id), "analysis": analysis}


@app.post("/process")
def process_image():
    """Receive image base64 from web app, analyze, store result."""
    data = request.json
    img_b64 = data["image"]

    image = img_b64 
    analysis = analyze_image(img_b64)

    db = get_db()
    readings = db["readings"]

    inserted_id = save_to_db(readings, image, analysis)

    return jsonify({"analysis": analysis, "id": str(inserted_id)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)