import os
import sys
import pytest
import json
from unittest.mock import patch
from requests.exceptions import RequestException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("app.requests.post")
@patch("app.database")
def test_receive_result_success(mock_db, mock_requests, client):
    """Mock ML service response"""
    mock_requests.return_value.json.return_value = {
        "gesture": "thumbs_up",
        "image_path": "/static/gestures/thumbs_up.png"
    }

    mock_db["readings"].find_one.return_value = {"_id": 123, "gesture": "thumbs_up"}

    response = client.post(
        "/receive_result",
        data=json.dumps({"image_base64": "fake_base64"}),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["gesture"] == "thumbs_up"
    assert data["image_path"] == "/static/gestures/thumbs_up.png"

@patch("app.requests.post")
def test_receive_result_no_image(mock_requests, client):
    """Test /receive_result with no image data"""
    response = client.post(
        "/receive_result",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

@patch("app.requests.post")
def test_receive_result_ml_service_failure(mock_requests, client):
    """Test /receive_result when ML service is down"""
    mock_requests.side_effect = RequestException("ML service down")

    response = client.post(
        "/receive_result",
        data=json.dumps({"image_base64": "fake_base64"}),
        content_type="application/json"
    )
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data
    assert "details" in data

@patch("app.database")
def test_api_results(mock_db, client):
    mock_db["analysis_results"].find.return_value.sort.return_value.limit.return_value = [
        {"_id": 1, "gesture": "thumbs_up"},
        {"_id": 2, "gesture": "peace"}
    ]

    response = client.get("/api/results")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["gesture"] == "thumbs_up"
    assert data[1]["gesture"] == "peace"
