from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class StudentSignUp(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    class_level: int = Field(1, ge=1, le=5)

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class StudentOut(BaseModel):
    id: int
    name: str
    email: str
    class_level: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
