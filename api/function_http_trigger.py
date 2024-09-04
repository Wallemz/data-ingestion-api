import azure.functions as func
import logging
from pydantic import ValidationError
from interfaces.sender_interface import MessageSender
from models.user_schema import UserSchema
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
