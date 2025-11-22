"""Unit tests for the Flask app routes."""

import os
import sys
import json
from unittest.mock import patch

from requests.exceptions import RequestException

import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # pylint: disable=C0413

from app import app

@pytest.fixture
def _test_client():
    """Flask test client fixture."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("app.requests.post")
@patch("app.database")
def test_receive_result_success(mock_db, mock_requests, _test_client):
    """Test /receive_result with a successful ML service response."""
    mock_requests.return_value.json.return_value = {
        "gesture": "thumbs_up",
        "image_path": "/static/gestures/thumbs_up.png"
    }

    mock_db["readings"].find_one.return_value = {"_id": 123, "gesture": "thumbs_up"}

    response = _test_client.post(
        "/receive_result",
        data=json.dumps({"image_base64": "fake_base64"}),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["gesture"] == "thumbs_up"
    assert data["image_path"] == "/static/gestures/thumbs_up.png"

@patch("app.requests.post")
def test_receive_result_no_image(_mock_requests, _test_client):
    """Test /receive_result route when no image data is provided."""
    response = _test_client.post(
        "/receive_result",
        data=json.dumps({}),
        content_type="application/json"
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

@patch("app.requests.post")
def test_receive_result_ml_service_failure(mock_requests, _test_client):
    """Test /receive_result when ML service is down."""
    mock_requests.side_effect = RequestException("ML service down")

    response = _test_client.post(
        "/receive_result",
        data=json.dumps({"image_base64": "fake_base64"}),
        content_type="application/json"
    )

    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data
    assert "details" in data

@patch("app.database")
def test_api_results(mock_db, _test_client):
    """Test /api/results endpoint."""
    mock_db["analysis_results"].find.return_value.sort.return_value.limit.return_value = [
        {"_id": 1, "gesture": "thumbs_up"},
        {"_id": 2, "gesture": "peace"}
    ]

    response = _test_client.get("/api/results")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["gesture"] == "thumbs_up"
    assert data[1]["gesture"] == "peace"
