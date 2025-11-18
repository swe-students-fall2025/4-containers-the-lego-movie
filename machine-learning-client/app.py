"""Machine learning client that simulates sensor readings and stores them in MongoDB."""

# currently some functions are commented out as i cant access web app yet
import base64
from datetime import datetime, timezone
from io import BytesIO

# from typing import Dict, Tuple

import cv2  # pylint: disable=import-error
import mediapipe as mp
import numpy as np
from pymongo import MongoClient
from flask import Flask

# add request and jsonify to flask
from PIL import Image

app = Flask(__name__)

mediapipe_hands = mp.solutions.hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5,
)
mediapipe_drawing = mp.solutions.drawing_utils

# utility functions


def decode_base64_to_cv2_image(image_base64: str) -> np.ndarray:
    # pylint: disable=undefined-variable
    """Decode a base64-encoded image string into an OpenCV BGR image."""
    image_bytes = base64.b64decode(image_base64)
    pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")
    numpy_image = np.array(pil_image)
    cv2_image = cv2.cvtColor(  # pylint: disable=no-member
        numpy_image, cv2.COLOR_RGB2BGR  # pylint: disable=no-member
    )
    return cv2_image


def classify_gesture_from_landmarks(
    hand_landmarks,
) -> str:  # pylint: disable=too-many-locals
    """Very simple heuristic gesture classifier based on Mediapipe landmarks.

    Returns one of:
    - 'thumbs_up'
    - 'thumbs_down'
    - 'peace'
    - 'fist'
    - 'open_hand'
    - 'unknown'
    """
    # Landmarks are normalized [0,1]; origin is top-left, so smaller y = higher on screen
    landmark_list = hand_landmarks.landmark

    wrist = landmark_list[0]
    thumb_tip = landmark_list[4]
    index_tip = landmark_list[8]
    middle_tip = landmark_list[12]
    ring_tip = landmark_list[16]
    pinky_tip = landmark_list[20]

    index_mcp = landmark_list[5]
    middle_mcp = landmark_list[9]
    ring_mcp = landmark_list[13]
    pinky_mcp = landmark_list[17]

    # Simple "extended finger" check: fingertip above its MCP joint
    def is_finger_extended(tip, mcp) -> bool:
        return tip.y < mcp.y - 0.02

    index_extended = is_finger_extended(index_tip, index_mcp)
    middle_extended = is_finger_extended(middle_tip, middle_mcp)
    ring_extended = is_finger_extended(ring_tip, ring_mcp)
    pinky_extended = is_finger_extended(pinky_tip, pinky_mcp)

    extended_fingers = [
        index_extended,
        middle_extended,
        ring_extended,
        pinky_extended,
    ]
    extended_count = sum(extended_fingers)

    # Thumb direction: compare thumb tip to wrist
    thumb_vertical_delta = thumb_tip.y - wrist.y

    # Heuristic rules
    if extended_count == 0:
        return "fist"

    if all(extended_fingers):
        # All four fingers extended; treat as open hand
        return "open_hand"

    if index_extended and middle_extended and not ring_extended and not pinky_extended:
        return "peace"

    # Thumb clearly above or below wrist → thumbs up/down
    if extended_count <= 1:
        if thumb_vertical_delta < -0.10:
            return "thumbs_up"
        if thumb_vertical_delta > 0.10:
            return "thumbs_down"
    # if unknown return unknown
    return "unknown"


def analyze_image(image_base64: str) -> str:
    """Analyze a base64 image using Mediapipe and return a gesture label."""
    cv2_image = decode_base64_to_cv2_image(image_base64)
    rgb_image = cv2.cvtColor(  # pylint: disable=no-member
        cv2_image, cv2.COLOR_BGR2RGB  # pylint: disable=no-member
    )

    results = mediapipe_hands.process(rgb_image)

    if not results.multi_hand_landmarks:
        return "no_hand_detected"

    hand_landmarks = results.multi_hand_landmarks[0]
    gesture_label = classify_gesture_from_landmarks(hand_landmarks)
    return gesture_label


# returns image for frontend to use
# def map_gesture_to_image_path(gesture_label: str) -> str:
#     """Map a gesture label to a static image path served by the web app.

#     The frontend can treat this as a relative URL and render the image.
#     """
#     # You can change this base directory to match your web app setup
#     base_path = "/static/gestures"

#     gesture_to_filename: Dict[str, str] = {
#         "thumbs_up": "thumbs_up.png",
#         "thumbs_down": "thumbs_down.png",
#         "peace": "peace.png",
#         "fist": "fist.png",
#         "open_hand": "open_hand.png",
#         "no_hand_detected": "no_hand.png",
#     }

#     filename = gesture_to_filename.get(gesture_label, "unknown.png")
#     # Join without creating filesystem paths (frontend just needs URL)
#     return f"{base_path}/{filename}"

# data base functions


def save_to_db(
    collection,
    image_base64: str,
    gesture_label: str,
    image_path: str,
) -> str:
    """Store metadata about the received image, detected gesture, and mapped asset."""
    document = {
        # Keep `analysis` for backward compatibility with earlier code/tests
        "analysis": gesture_label,
        "gesture": gesture_label,
        "image_path": image_path,
        "timestamp": datetime.now(timezone.utc),
        "image_length": len(image_base64),
    }
    result = collection.insert_one(document)
    return str(result.inserted_id)


def get_db():
    """Get from db"""
    client = MongoClient("mongodb://mongodb:27017")
    return client["ml_db"]


# main function used by frontend


# def process_incoming_image(image_base64: str) -> Dict[str, str]:
#     """Called by the web app to process a single frame."""
#     gesture_label = analyze_image(image_base64)
#     image_path = map_gesture_to_image_path(gesture_label)

#     database = get_db()
#     readings_collection = database["readings"]

#     inserted_id = save_to_db(
#         readings_collection,
#         image_base64=image_base64,
#         gesture_label=gesture_label,
#         image_path=image_path,
#     )

#     return {
#         "id": inserted_id,
#         "gesture": gesture_label,
#         "image_path": image_path,
#     }


# @app.post("/process")
# def process_image():
#     """Receive base64 image from web app, analyze gesture, store result, return metadata."""
#     request_data = request.get_json(force=True)
#     image_base64 = request_data["image"]

#     result = process_incoming_image(image_base64)
#     return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
