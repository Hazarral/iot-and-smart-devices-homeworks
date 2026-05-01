import time
import random

# This part is 15-16
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

# This part is 18

# --- MOCKED HARDWARE & CLOUD FUNCTIONS ---
def read_distance():
    # Mocks an ultrasonic sensor reading in cm
    return random.uniform(5.0, 50.0)

def trigger_camera():
    print("CAMERA: Image captured.")
    return "fruit_image.jpg"

def send_telemetry_to_hub(key, value):
    print(f"IOT HUB -> Telemetry sent: {key} = {value}")

def receive_hub_command(expected_command):
    # Mocks receiving a Direct Method command from Azure IoT Hub/Functions
    print(f"IOT HUB <- Command received: '{expected_command}'")
    return True

def set_led(state):
    print(f"LED: Turned {'ON' if state else 'OFF'}")

# --- MAIN SYSTEM LOOP ---
def run_fruit_quality_detector():
    PROXIMITY_THRESHOLD_CM = 15.0
    
    print("System started. Monitoring conveyor belt...")
    
    while True:
        distance = read_distance()
        time.sleep(1) # Sensor read delay
        
        if distance < PROXIMITY_THRESHOLD_CM:
            print(f"\n[ALERT] Object detected at {distance:.1f} cm!")
            
            # 1. Monitor proximity and send data to IoT Hub
            send_telemetry_to_hub("proximity_cm", distance)
            
            # 2. Trigger the camera via a command (simulating Hub responding to proximity)
            if receive_hub_command("capture_image"):
                image_path = trigger_camera()
                
                # 3. Classify using Edge model
                print("EDGE AI: Classifying image...")
                results = classify_image(image_path)
                best_match = max(results['predictions'], key=lambda x: x['probability'])
                fruit_tag = best_match['tagName']
                
                # 4. Send results to IoT Hub
                send_telemetry_to_hub("classification_result", fruit_tag)
                
                # 5. Turn LED on/off depending on results via command
                if "unripe" in fruit_tag:
                    if receive_hub_command("turn_led_on"):
                        set_led(True)
                else:
                    if receive_hub_command("turn_led_off"):
                        set_led(False)
                        
            print("Processing complete. Waiting for next object...\n")
            time.sleep(3) # Wait before scanning next item
            
        # Break added just to prevent infinite loop in this mock execution
        break 

# Run the prototype
run_fruit_quality_detector()