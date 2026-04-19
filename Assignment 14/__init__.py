import logging
import azure.functions as func
import json

def main(req: func.HttpRequest, smsMessage: func.Out[func.TwilioSmsMessage]) -> func.HttpResponse:
    req_body = req.get_json()
    
    # Geofence logic (Example logic based on payload)
    distance_to_center = req_body.get('distance')
    is_inside_geofence = distance_to_center < 100 # meters
    
    if is_inside_geofence:
        logging.info("Asset entered geofence. Triggering SMS.")
        
        # Structure required by the Azure Twilio binding
        msg = {
            "body": "ALERT: Your IoT device has entered the designated geofence.",
            "to": "+19876543210" # Target phone number
        }
        smsMessage.set(json.dumps(msg))
        
        return func.HttpResponse("Inside geofence. SMS Sent.", status_code=200)
        
    return func.HttpResponse("Outside geofence. No action taken.", status_code=200)