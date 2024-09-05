import azure.functions as func
import json
import logging
import os
from interfaces.persistence_interface import PersistenceServiceInterface
from models.user_schema import UserSchema
from services.cosmos_db_service import CosmosDBService

SERVICE_BUS_SUBSCRIPTION = os.getenv("SERVICE_BUS_SUBSCRIPTION")
SERVICE_BUS_TOPIC = os.getenv("SERVICE_BUS_TOPIC")

persistence_service: PersistenceServiceInterface = CosmosDBService()
svbus_trigger_bp = func.Blueprint()

@svbus_trigger_bp.service_bus_topic_trigger(arg_name="azservicebus", 
                                            topic_name=SERVICE_BUS_TOPIC,
                                            subscription_name=SERVICE_BUS_SUBSCRIPTION,
                                            connection="SERVICE_BUS_CONNECTION_STRING")
def servicebus_topic_trigger(azservicebus: func.ServiceBusMessage):
    logging.info('Python ServiceBus Topic trigger received a message.')

    try:
        # Data validation
        message_body = azservicebus.get_body().decode('utf-8')
        message_data = json.loads(message_body)
        user_data = UserSchema(**message_data)
        logging.info(f"Valid user data received for user {user_data.userId}.")

        # Save data to persistence layer
        persistence_service.save_user_data(user_data)
        logging.info(f"Data for user {user_data.userId} ingested successfully into Cosmos DB.")

    except json.JSONDecodeError as json_error:
        logging.error(f"Failed to decode JSON message: {str(json_error)}")
    except Exception as e:
        logging.error(f"Error processing Service Bus message: {str(e)}")
        raise