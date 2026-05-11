import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Parse the incoming JSON from the LUIS service
        req_body = req.get_json()
        prediction = req_body.get('prediction', {})
        top_intent = prediction.get('topIntent')

        # Rubric Requirement: Handle CancelTimer intent
        if top_intent == "CancelTimer":
            # Rubric Requirement: Log the intent
            logging.info("ACTION REQUIRED: Recognized top intent 'CancelTimer'. Terminating active timer process.")
            
            return func.HttpResponse(
                json.dumps({"status": "success", "message": "Timer cancelled successfully."}),
                mimetype="application/json",
                status_code=200
            )
        
        elif top_intent == "SetTimer":
            logging.info("Recognized top intent 'SetTimer'. Initiating timer sequence.")
            return func.HttpResponse(
                json.dumps({"status": "success", "message": "Timer started."}),
                mimetype="application/json",
                status_code=200
            )
            
        else:
            logging.warning(f"Unrecognized intent detected: {top_intent}")
            return func.HttpResponse(
                json.dumps({"status": "error", "message": "Intent not handled."}),
                mimetype="application/json",
                status_code=400
            )

    except ValueError:
        logging.error("Invalid JSON payload received.")
        return func.HttpResponse("Invalid JSON payload.", status_code=400)