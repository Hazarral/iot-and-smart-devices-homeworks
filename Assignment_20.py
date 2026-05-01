import time

# Previously, we used the cloud endpoint provided by Azure Custom Vision:
# CLOUD_API_URL = "https://<region>.api.cognitive.microsoft.com/customvision/v3.0/Prediction/..."

# Now, we use the local endpoint of the Edge container running on the device (e.g., Raspberry Pi)
EDGE_CONTAINER_URL = "http://127.0.0.1:80/image"

def capture_image_from_camera():
    print("CAMERA: Capturing frame from conveyor belt...")
    time.sleep(0.5) # Simulate capture delay
    return "current_frame.jpg"

def detect_objects_on_edge(image_path):
    print(f"NETWORK: Sending '{image_path}' to local edge container at {EDGE_CONTAINER_URL}")
    
    # In a real scenario, this would be:
    # with open(image_path, 'rb') as f:
    #     response = requests.post(EDGE_CONTAINER_URL, data=f.read())
    # return response.json()
    
    # Mocking the response from the local Docker container running the compact model
    return {
        "id": "local-edge-inferencing-id",
        "project": "stock-detector-edge",
        "iteration": "Iteration3-Compact",
        "created": "2026-05-01T14:42:01.000Z",
        "predictions": [
            {"tagName": "banana", "probability": 0.85, "boundingBox": {"left": 0.4, "top": 0.2, "width": 0.2, "height": 0.6}}
        ]
    }

# --- Main Edge Execution Loop ---
def run_edge_inference():
    print("--- Starting Edge Object Detection ---")
    image_to_process = capture_image_from_camera()
    
    start_time = time.time()
    results = detect_objects_on_edge(image_to_process)
    end_time = time.time()
    
    latency = (end_time - start_time) * 1000 # Convert to milliseconds
    
    if results:
        top_prediction = max(results['predictions'], key=lambda x: x['probability'])
        print("\n--- Edge Prediction Success ---")
        print(f"Detected Object: {top_prediction['tagName']}")
        print(f"Confidence: {(top_prediction['probability'] * 100):.1f}%")
        print(f"Network Latency: {latency:.2f} ms (Ultra-low due to local execution)")
    else:
        print("Failed to get prediction from edge container.")

run_edge_inference()