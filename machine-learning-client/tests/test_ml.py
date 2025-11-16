"""Unit tests for the machine learning helper functions."""

from unittest.mock import MagicMock

from app import collect_data, analyze_data, save_to_db


def test_collect_data():
    """collect_data should return a mapping with a float value and timestamp."""
    collected_data = collect_data()
    assert "value" in collected_data
    assert "timestamp" in collected_data
    assert isinstance(collected_data["value"], float)


def test_analyze_data_low():
    """analyze_data should classify low values as 'low'."""
    assert analyze_data(0.2) == "low"


def test_analyze_data_high():
    """analyze_data should classify high values as 'high'."""
    assert analyze_data(0.9) == "high"


def test_save_to_db():
    """save_to_db should insert a document with value, analysis, and timestamp."""
    fake_collection = MagicMock()

    inserted_id = save_to_db(fake_collection, 0.7, "high")

    fake_collection.insert_one.assert_called_once()
    (
        call_args,
        unused_kwargs,
    ) = fake_collection.insert_one.call_args  # pylint: disable=unused-variable

    inserted_document = call_args[0]
    assert inserted_document["value"] == 0.7
    assert inserted_document["analysis"] == "high"
    assert "timestamp" in inserted_document

    assert inserted_id is not None
