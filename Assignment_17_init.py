# __init__.py (Inside the Azure Function Edge Module)
import json
import logging
import azure.functions as func

def main(event: func.EventHubEvent):
    # This function runs on the edge, triggered by telemetry from the camera module
    message_body = event.get_body().decode('utf-8')
    logging.info(f"Edge Function received message: {message_body}")
    
    data = json.loads(message_body)
    
    if 'detected_fruit' in data:
        fruit_state = data['detected_fruit']
        
        # Determine if we need to send a command to the LED module
        if "unripe" in fruit_state:
            logging.info("Edge Function sending command: TURN ON REJECTION LED")
            # Code to invoke direct method on LED module would go here
        else:
            logging.info("Edge Function sending command: TURN OFF REJECTION LED")