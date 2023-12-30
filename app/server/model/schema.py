from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Schema of User 

class UserSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "abc@gmail.com",
                "password": "abc123"
            }
        }

# Schema of request 

class RequestSchema(BaseModel):
    user_id: str = Field(...)
    doc_url: str = Field(...)
    doc_name: str = Field(...)
    is_valid: bool
    timestamp: datetime

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "doc_url": "https://example.com",
                "doc_name": "example_document",
                "is_valid": True,
                "timestamp": "2023-01-01T00:00:00"
            }
        }

# Schema of response

class ResponseSchema(BaseModel):
    user_id: str = Field(...)
    request_id: str = Field(...)
    prompt: str = Field(...)
    ml_response: str = Field(...)
    isSuccess: bool = Field(...)
    timestamp: datetime

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "request_id": "request456",
                "prompt": "What is the meaning of life?",
                "ml_response": "42",
                "isSuccess": True,
                "timestamp": datetime.now(),
                
            },
            

        }


# respoonseModel function

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


