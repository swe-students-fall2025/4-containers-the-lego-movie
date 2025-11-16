"""Machine learning client that simulates sensor readings and stores them in MongoDB."""

import time
import random
from datetime import datetime, timezone

from flask import Flask
from pymongo import MongoClient


def collect_data():
    """Simulate collecting a sensor reading.

    Returns a dictionary with a random float value and a UTC timestamp.
    """
    return {
        "value": random.random(),
        "timestamp": datetime.now(timezone.utc),
    }


def analyze_data(value):
    """Classify a numeric value as either 'high' or 'low'.

    Values greater than 0.5 are classified as 'high', all others as 'low'.
    """
    return "high" if value > 0.5 else "low"


def save_to_db(collection, value, analysis):
    """Insert a reading document into the given MongoDB collection.

    Args:
        collection: A MongoDB collection object.
        value: The numeric reading value.
        analysis: The classification label for the value.

    Returns:
        The inserted document's id.
    """
    document = {
        "value": value,
        "analysis": analysis,
        "timestamp": datetime.now(timezone.utc),
    }
    result = collection.insert_one(document)
    return result.inserted_id


def get_db():
    """Return a handle to the MongoDB database used by the ML client."""
    client = MongoClient("mongodb://mongodb:27017")
    return client["ml_db"]


def main():
    """Continuously collect, analyze, and store sensor readings."""
    database = get_db()
    readings_collection = database["readings"]

    while True:
        raw_reading = collect_data()
        analysis = analyze_data(raw_reading["value"])

        inserted_id = save_to_db(
            readings_collection,
            raw_reading["value"],
            analysis,
        )

        print(
            f"Inserted: value={raw_reading['value']:.3f}, "
            f"analysis={analysis}, id={inserted_id}",
        )

        time.sleep(3)


if __name__ == "__main__":
    main()
