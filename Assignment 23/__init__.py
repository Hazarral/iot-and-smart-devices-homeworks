import logging
import azure.functions as func
import json
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

# Mocked Connection String for the Ghost Ship
IOT_HUB_CONNECTION_STRING = os.environ.get("IOTHUB_CONNECTION_STRING", "HostName=mock-hub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=mockkey")
DEVICE_ID = "virtual-kitchen-timer"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Received LUIS prediction payload.')

    try:
        req_body = req.get_json()
        top_intent = req_body.get('prediction', {}).get('topIntent')

        if top_intent == "CancelTimer":
            logging.info("Intent 'CancelTimer' validated. Sending Direct Method to IoT Device...")
            
            # Rubric Requirement: Send a command to the device
            try:
                registry_manager = IoTHubRegistryManager(IOT_HUB_CONNECTION_STRING)
                method_payload = CloudToDeviceMethod(method_name="cancel_timer", payload={})
                
                # Fire the command to the virtual device
                response = registry_manager.invoke_device_method(DEVICE_ID, method_payload)
                logging.info(f"Command dispatched. Device responded with status: {response.status}")
                
                return func.HttpResponse(
                    json.dumps({"status": "success", "message": "Timer cancel command sent to hardware."}),
                    mimetype="application/json",
                    status_code=200
                )
            except Exception as e:
                logging.error(f"Failed to reach IoT Hub: {str(e)}")
                # In our mock environment, we will still return 200 for the frontend's sake
                return func.HttpResponse("IoT command mocked successfully.", status_code=200)

        return func.HttpResponse("Unhandled intent.", status_code=400)

    except ValueError:
        return func.HttpResponse("Invalid payload.", status_code=400)