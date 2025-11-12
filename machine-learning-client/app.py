import time
import random
from datetime import datetime
from pymongo import MongoClient

def collect_data():
    return {"value": random.random(), "timestamp": datetime.now()}

def analyze_data(data):
    data["analysis"] = "high" if data["value"] > 0.5 else "low"
    return data

def main():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["ml_db"]
    collection = db["readings"]

    while True:
        data = collect_data()
        analyzed = analyze_data(data)
        collection.insert_one(analyzed)
        print("✅ Inserted data:", analyzed)
        time.sleep(5)  

if __name__ == "__main__":
    main()
