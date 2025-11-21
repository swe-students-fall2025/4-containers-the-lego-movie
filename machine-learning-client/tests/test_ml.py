"""Unit tests for the machine learning helper functions."""
import sys
import os
import base64
import io
from PIL import Image
from unittest.mock import MagicMock, patch
import pytest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import (
    decode_base64_to_cv2_image,
    classify_gesture_from_landmarks,
    analyze_image,
    map_gesture_to_image_path,
    save_to_db,
    process_incoming_image,
)

# Create dummy image
def create_dummy_image_base64(width = 64, height = 64, color = (255, 0, 0)) -> str:
    import cv2

    img = np.full((height, width, 3), color, dtype=np.uint8)
    pil_image = Image.fromarray(img)
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')

# Test decode_base64_to_cv2_image

def test_decode_base64_to_cv2_image():
    """decode_base64_to_cv2_image should return a valid cv2 image array."""
    dummy_base64 = create_dummy_image_base64()
    cv2_image = decode_base64_to_cv2_image(dummy_base64)
    assert cv2_image.shape == (64, 64, 3)
    assert cv2_image.dtype == np.uint8

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
