from abc import ABC, abstractmethod
from models.user_schema import UserSchema

class MessageSender(ABC):
    """Interface for sending messages to different destinations."""
    
    @abstractmethod
    def send_message(self, user_data: UserSchema) -> None:
        """Send user data to the defined destination."""
        pass