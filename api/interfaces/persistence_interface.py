from abc import ABC, abstractmethod
from models.user_schema import UserSchema

class PersistenceServiceInterface(ABC):
    @abstractmethod
    def save_user_data(self, user_data: UserSchema) -> None:
        """Save user data to the persistence layer"""
        pass
