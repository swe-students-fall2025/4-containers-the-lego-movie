import tests
from unittest.mock import MagicMock
from app import collect_data, analyze_data, save_to_db


def test_collect_data():
    data = collect_data()
    assert "value" in data
    assert "timestamp" in data
    assert isinstance(data["value"], float)


def test_analyze_data_low():
    assert analyze_data(0.2) == "low"


def test_analyze_data_high():
    assert analyze_data(0.9) == "high"


def test_save_to_db():
    fake_collection = MagicMock()

    inserted_id = save_to_db(fake_collection, 0.7, "high")

    fake_collection.insert_one.assert_called_once()
    args, kwargs = fake_collection.insert_one.call_args

    inserted_doc = args[0]
    assert inserted_doc["value"] == 0.7
    assert inserted_doc["analysis"] == "high"
    assert "timestamp" in inserted_doc

    assert inserted_id is not None
