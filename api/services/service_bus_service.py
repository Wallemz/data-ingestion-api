import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from interfaces.sender_interface import MessageSender
from models.user_schema import UserSchema

class ServiceBusService(MessageSender):
    """Implementation of MessageSender for Azure Service Bus."""
    
    def __init__(self):
        self.connection_str = os.getenv("SERVICE_BUS_CONNECTION_STRING")
        self.topic_name = os.getenv("SERVICE_BUS_TOPIC")
        if not self.connection_str or not self.topic_name:
            raise ValueError("Service Bus connection string or topic name is missing.")
    
    def send_message(self, user_data: UserSchema) -> None:
        """Send a message with user data to the Service Bus topic."""
        message_data = user_data.model_dump_json()
        servicebus_client = ServiceBusClient.from_connection_string(self.connection_str)

        try:
            with servicebus_client.get_topic_sender(self.topic_name) as sender:
                message = ServiceBusMessage(message_data)
                sender.send_messages(message)
        except Exception as e:
            raise RuntimeError(f"Error sending message to Service Bus: {str(e)}")