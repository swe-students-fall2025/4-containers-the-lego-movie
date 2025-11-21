"""Unit tests for the machine learning helper functions."""
import sys
import os
import io
import base64
from unittest.mock import MagicMock, patch

import numpy as np
from PIL import Image

from app import (
    decode_base64_to_cv2_image,
    # classify_gesture_from_landmarks,
    # analyze_image,
    map_gesture_to_image_path,
    save_to_db,
    process_incoming_image,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create dummy image
def create_dummy_image_base64(width = 64, height = 64, color = (255, 0, 0)) -> str:
    """Create a dummy base64 encoded image for testing."""
    img = np.full((height, width, 3), color, dtype=np.uint8)
    pil_image = Image.fromarray(img)
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')

# Test decode_base64_to_cv2_image
def test_decode_base64_to_cv2_image():
    """Check base64 image is decoded correctly into OpenCV format."""
    dummy_base64 = create_dummy_image_base64()
    cv2_image = decode_base64_to_cv2_image(dummy_base64)
    assert cv2_image.shape == (64, 64, 3)
    assert cv2_image.dtype == np.uint8

# Test classify_gesture_from_landmarks
# pylint: disable=too-few-public-methods
class MockLandmark:
    """Mock class for a single landmark with x and y coordinates."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
class MockHandLandmarks:
    """Mock class for hand landmarks."""
    def __init__(self, landmarks):
        self.landmark = landmarks

def make_landmarks(ys):
    return MockHandLandmarks([MockLandmark(0, y) for y in ys])

# Test map_gesture_to_image_path
def test_map_gesture_to_image_path():
    """Check that gesture labels map to correct image paths."""
    path = map_gesture_to_image_path("thumbs_up")
    assert path.endswith("thumbs_up.png")
    unknown_path = map_gesture_to_image_path("nonexistent")
    assert unknown_path.endswith("unknown.png")

# Test save_to_db
def test_save_to_db():
    """Check that save_to_db inserts the correct document."""
    mock_collection = MagicMock()
    mock_collection.insert_one.return_value.inserted_id = "123"
    inserted_id = save_to_db(
        mock_collection,
        "base64data",
        "thumbs_up",
        "/static/gestures/thumbs_up.png",
    )
    assert inserted_id == "123"
    mock_collection.insert_one.assert_called_once()

# Test process_incoming_image
@patch("app.get_db")
@patch("app.analyze_image")
def test_process_incoming_image(mock_analyze_image, mock_get_db):
    """Check that process_incoming_image works end-to-end."""
    mock_analyze_image.return_value = "thumbs_up"

    mock_collection = MagicMock()
    mock_collection.insert_one.return_value.inserted_id = "abc123"
    mock_db = {"readings": mock_collection}
    mock_get_db.return_value = mock_db

    img_b64 = create_dummy_image_base64()
    result = process_incoming_image(img_b64)

    assert result["gesture"] == "thumbs_up"
    assert result["image_path"].endswith("thumbs_up.png")
    assert result["id"] == "abc123"

# def test_collect_data():
#     """collect_data should return a mapping with a float value and timestamp."""
#     collected_data = collect_data()
#     assert "value" in collected_data
#     assert "timestamp" in collected_data
#     assert isinstance(collected_data["value"], float)


# def test_analyze_data_low():
#     """analyze_data should classify low values as 'low'."""
#     assert analyze_image(0.2) == "low"


# def test_analyze_data_high():
#     """analyze_data should classify high values as 'high'."""
#     assert analyze_image(0.9) == "high"


# def test_save_to_db():
#     """save_to_db should insert a document with value, analysis, and timestamp."""
#     fake_collection = MagicMock()

#     inserted_id = save_to_db(fake_collection, 0.7, "high")

#     fake_collection.insert_one.assert_called_once()
#     (
#         call_args,
#         unused_kwargs,
#     ) = fake_collection.insert_one.call_args  # pylint: disable=unused-variable

#     inserted_document = call_args[0]
#     assert inserted_document["value"] == 0.7
#     assert inserted_document["analysis"] == "high"
#     assert "timestamp" in inserted_document

#     assert inserted_id is not None
