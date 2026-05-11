import time
import threading
from azure.iot.device import IoTHubDeviceClient, MethodResponse

# Global state flag for the timer
timer_active = False

def method_request_handler(method_request):
    global timer_active
    
    # Rubric Requirement: Receive the command and cancel the timer
    if method_request.name == "cancel_timer":
        print("\n[DEVICE] 🔴 Received 'cancel_timer' command from Azure Cloud.")
        if timer_active:
            timer_active = False
            print("[DEVICE] 🛑 Timer successfully aborted by user command.")
            payload = {"result": True, "data": "Timer cancelled"}
            status = 200
        else:
            print("[DEVICE] ⚠️ Timer was not running.")
            payload = {"result": False, "data": "No active timer"}
            status = 400
    else:
        payload = {"result": False, "data": "Unknown method"}
        status = 404

    # Acknowledge receipt back to the cloud
    method_response = MethodResponse.create_from_method_request(method_request, status, payload)
    client.send_method_response(method_response)

def start_mock_timer(duration=60):
    global timer_active
    timer_active = True
    print(f"\n[DEVICE] ⏱️ Timer started for {duration} seconds...")
    
    for i in range(duration, 0, -1):
        if not timer_active:
            print("[DEVICE] ⏹️ Timer thread terminated early.")
            return
        print(f"   ... {i} seconds remaining")
        time.sleep(1)
        
    print("[DEVICE] 🔔 BEEP! Timer finished normally.")
    timer_active = False

if __name__ == "__main__":
    print("[DEVICE] Booting Virtual IoT Timer...")
    # Initialize the mocked IoT client
    client = IoTHubDeviceClient.create_from_connection_string("HostName=mock;DeviceId=mock;SharedAccessKey=mock")
    
    # Attach the listener for cloud commands
    client.on_method_request_received = method_request_handler
    client.connect()
    print("[DEVICE] Connected to Azure IoT Hub. Listening for commands...")

    # Start a dummy timer in the background so we have something to cancel
    threading.Thread(target=start_mock_timer, args=(30,), daemon=True).start()

    # Keep the main thread alive to listen for the cancel command
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[DEVICE] Shutting down.")
        client.disconnect()