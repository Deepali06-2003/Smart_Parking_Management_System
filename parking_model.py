import cv2
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input


MODEL_PATH = "resnet50_parking.keras"

model = load_model(MODEL_PATH)


def predict_slot(slot):

    slot = cv2.resize(slot, (224, 224))

    slot = cv2.cvtColor(
        slot,
        cv2.COLOR_BGR2RGB
    )

    slot = img_to_array(slot)

    slot = np.expand_dims(slot, axis=0)

    slot = preprocess_input(slot)

    prediction = model.predict(
        slot,
        verbose=0
    )[0][0]

    if prediction >= 0.5:
        return "Occupied", float(prediction)

    else:
        return "Empty", float(1 - prediction)


def analyze_parking(image, parking_slots):

    empty_count = 0
    occupied_count = 0

    results = []

    # Make a copy so original image is not changed
    annotated_image = image.copy()

    for i, (x1, y1, x2, y2) in enumerate(parking_slots):

        # Crop parking slot
        slot = image[y1:y2, x1:x2]

        # Predict
        status, confidence = predict_slot(slot)

        # Count
        if status == "Empty":
            empty_count += 1
            color = (0, 255, 0)       # Green

        else:
            occupied_count += 1
            color = (0, 0, 255)       # Red

        # Draw rectangle
        cv2.rectangle(
            annotated_image,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        # Slot number
        label = f"{i + 1}: {status}"

        cv2.putText(
            annotated_image,
            label,
            (x1, max(y1 - 5, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )

        results.append({
            "slot": i + 1,
            "status": status,
            "confidence": round(confidence, 4)
        })

    total_slots = len(parking_slots)

    occupancy_rate = (
        occupied_count / total_slots * 100
        if total_slots > 0
        else 0
    )

    return {
        "total_slots": total_slots,
        "empty_slots": empty_count,
        "occupied_slots": occupied_count,
        "occupancy_rate": round(occupancy_rate, 2),
        "slots": results,
        "annotated_image": annotated_image
    }