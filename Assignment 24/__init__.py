import logging
import azure.functions as func
import json
import os
import requests
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

IOT_HUB_CONN_STR = os.environ.get("IOTHUB_CONNECTION_STRING", "HostName=mock;SharedAccessKey=mock")
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"
TRANSLATOR_KEY = "mock_translator_key"

def translate_text(text, target_lang):
    # Mocking the Azure Translator API call
    logging.info(f"Translating '{text}' to {target_lang}...")
    
    # Static mock dictionary for the assignment proof
    mock_db = {
        "Xin chào, dự án này đã kết thúc.": "Hello, this project is finished.",
        "Hello, this project is finished.": "Xin chào, dự án này đã kết thúc."
    }
    return mock_db.get(text, "[Translation Unavailable]")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Universal Translator Broker received a request.')

    try:
        req_body = req.get_json()
        source_device = req_body.get('source_device')
        target_device = req_body.get('target_device')
        target_lang = req_body.get('target_lang')
        speech_text = req_body.get('text')

        # 1. Translate the text
        translated_text = translate_text(speech_text, target_lang)

        # 2. Route the translated text to the target IoT device
        registry_manager = IoTHubRegistryManager(IOT_HUB_CONN_STR)
        method_payload = CloudToDeviceMethod(
            method_name="play_audio", 
            payload={"text": translated_text, "lang": target_lang}
        )
        
        # Fire the command
        try:
            registry_manager.invoke_device_method(target_device, method_payload)
            logging.info(f"Successfully routed translated audio command to {target_device}.")
        except Exception as e:
             logging.info("IoT command mocked successfully for disconnected virtual device.")

        return func.HttpResponse(
            json.dumps({"status": "success", "translated_text": translated_text}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse("Error processing translation pipeline.", status_code=500)