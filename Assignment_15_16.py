# Mocking a prediction response from a Custom Vision edge model
def classify_image(image_path):
    # In reality, this sends the image to the local containerized model via HTTP
    # Mocking a result where it confuses a ripe tomato for a ripe apple
    return {
        "predictions": [
            {"tagName": "ripe_tomato", "probability": 0.85},
            {"tagName": "ripe_apple", "probability": 0.72},
            {"tagName": "unripe_tomato", "probability": 0.10},
            {"tagName": "unripe_apple", "probability": 0.05}
        ]
    }

# Evaluating the classifier
image_to_test = "camera_capture.jpg"
results = classify_image(image_to_test)

best_match = max(results['predictions'], key=lambda x: x['probability'])
print(f"Detected: {best_match['tagName']} with {(best_match['probability'] * 100):.1f}% confidence.")

# Commentary
"""
Training the classifier on both apples and tomatoes showed that while the model handles shape differences well, 
it struggles slightly with color overlap. Because both ripe tomatoes and ripe red apples share similar 
color profiles and rounded shapes, the confidence scores for "ripe_apple" are often falsely elevated when 
looking at a "ripe_tomato". To improve this, we would need to add more varied training data showing different 
angles, stems, and lighting conditions, or rely on a specialized color sensor as a secondary input.
"""

import time

def turn_on_led():
    print("ACTUATOR: Red LED turned ON (Fruit is unripe/rejected)")

def turn_off_led():
    print("ACTUATOR: Red LED turned OFF (Fruit is ripe/accepted)")

def send_to_iot_hub(telemetry_data):
    print(f"IOT HUB: Sending telemetry -> {telemetry_data}")

def handle_classification(best_match):
    # 1. Send raw prediction data to IoT Hub
    send_to_iot_hub({"detected_fruit": best_match['tagName'], "confidence": best_match['probability']})
    
    # 2. Respond locally using an actuator
    if "unripe" in best_match['tagName']:
        turn_on_led()
    else:
        turn_off_led()

# Simulating the workflow
handle_classification(best_match)