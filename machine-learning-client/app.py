import time
import random
from datetime import datetime, timezone
from pymongo import MongoClient


def collect_data():
    """Fake ML sensor --> simulates sensor"""
    return {
        "value": random.random(),
        "timestamp": datetime.now(timezone.utc)
    }


def analyze_data(value):
    """classification"""
    return "high" if value > 0.5 else "low"


def save_to_db(collection, value, analysis):
    doc = {
        "value": value,
        "analysis": analysis,
        "timestamp": datetime.now(timezone.utc)
    }
    result = collection.insert_one(doc)
    return result.inserted_id


def get_db():
    client = MongoClient("mongodb://mongodb:27017")
    return client["ml_db"]


def main():
    db = get_db()
    readings = db["readings"]

    while True:
        raw = collect_data()
        analysis = analyze_data(raw["value"])

        inserted_id = save_to_db(readings, raw["value"], analysis)

        print(
            f"Inserted: value={raw['value']:.3f}, "
            f"analysis={analysis}, id={inserted_id}"
        )

        time.sleep(3)


if __name__ == "__main__":
    main()
