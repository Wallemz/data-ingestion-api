from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    userId: str = Field(..., description="Unique identifier for the user")
    email: EmailStr = Field(..., description="User's email address")
    firstName: str = Field(..., description="First name of the user")
    lastName: str = Field(..., description="Last name of the user")
    flightId: str = Field(..., description="Flight identifier for the user")

    class Config:
        schema_extra = {
            "example": {
                "userId": "user_123",
                "email": "user@example.com",
                "firstName": "Alice",
                "lastName": "Doe",
                "flightId": "flight_456"
            }
        }