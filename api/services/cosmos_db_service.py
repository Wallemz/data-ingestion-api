import os
import uuid
from azure.cosmos import CosmosClient
from models.user_schema import UserSchema
from interfaces.persistence_interface import PersistenceServiceInterface

class CosmosDBService(PersistenceServiceInterface):
    def __init__(self):
        self.endpoint = os.getenv("COSMOS_DB_ENDPOINT")
        self.key = os.getenv("COSMOS_DB_KEY")
        self.database_name = os.getenv("COSMOS_DB_DATABASE")
        self.container_name = os.getenv("COSMOS_DB_CONTAINER")

        if not self.endpoint or not self.key:
            raise ValueError("Cosmos DB connection info is missing.")
        
        self.client = CosmosClient(self.endpoint, self.key)
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def save_user_data(self, user_data: UserSchema) -> None:
        """Save user data into Cosmos DB"""
        try:
            user_data_dict = user_data.model_dump()
            if 'id' not in user_data_dict:
                user_data_dict['id'] = str(uuid.uuid4())
            self.container.create_item(body=user_data_dict)
        except Exception as e:
            raise RuntimeError(f"Error saving data to Cosmos DB: {str(e)}")
