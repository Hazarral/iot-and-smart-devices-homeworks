import logging
import azure.functions as func

def main(req: func.HttpRequest, outputBlob: func.Out[str]) -> func.HttpResponse:
    logging.info('Processing GPS data upload.')
    
    # Assume the body contains the GPS data payload
    gps_data = req.get_body().decode('utf-8')
    
    # Write to Blob Storage
    outputBlob.set(gps_data)

    return func.HttpResponse("GPS data successfully saved to Blob Storage.", status_code=200)