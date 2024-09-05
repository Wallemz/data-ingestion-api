import azure.functions as func
import json
import logging
from interfaces.sender_interface import MessageSender
from models.user_schema import UserSchema
from pydantic import ValidationError
from services.cosmos_db_service import CosmosDBService
from services.service_bus_service import ServiceBusService

http_trigger_bp = func.Blueprint() 

@http_trigger_bp.route(route="user_data", methods=["POST"])
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request for user data.')

    # Body request check
    try:
        req_body = req.get_json()
        user_data = UserSchema(**req_body)  # Pydantic model validation
    except ValidationError as ve:
        logging.error(f"Validation error: {ve.json()}")
        return func.HttpResponse(f"Validation error: {ve.json()}", status_code=400)
    except ValueError:
        logging.error("Invalid JSON format.")
        return func.HttpResponse("Invalid JSON format.", status_code=400)

    # Send user data to Service Bus
    message_sender: MessageSender = ServiceBusService()
    try:
        message_sender.send_message(user_data)
        logging.info(f"User data sent successfully: {user_data}")
        return func.HttpResponse(f"User data sent successfully: {user_data.userId}", status_code=200)
    except RuntimeError as e:
        logging.error(f"Error sending message: {e}")
        return func.HttpResponse("Failed to send message.", status_code=500)

@http_trigger_bp.route(route="user_data", methods=["GET"])
def http_get_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing GET request for user data.')

    # Extract userId
    user_id = req.params.get('userId')
    if not user_id:
        logging.error("userId is required in the query parameters.")
        return func.HttpResponse("userId is required in the query parameters.", status_code=400)

    # Cosmos DB Query
    cosmos_db_service = CosmosDBService()
    try:
        user_data = cosmos_db_service.get_user_data(user_id)
        if user_data:
            logging.info(f"User data retrieved successfully for userId: {user_id}")
            return func.HttpResponse(json.dumps(user_data), status_code=200, mimetype="application/json")
        else:
            logging.info(f"No user data found for userId: {user_id}")
            return func.HttpResponse("User not found.", status_code=404)
    except Exception as e:
        logging.error(f"Error retrieving data from Cosmos DB: {str(e)}")
        return func.HttpResponse("Failed to retrieve data.", status_code=500)