from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime, timedelta
import re



class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    hashed_password: Optional[str] = None
    disabled: bool = False
    role: str = Field("user", pattern="^(user|admin)$")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('name')
    def validate_name(cls, v):
        if not re.match(r'^[a-zA-Z\s-]+$', v):
            raise ValueError('Name can only contain letters, spaces, and hyphens')
        return v.strip()

    @validator('full_name')
    def validate_full_name(cls, v):
        if v is not None:
            if not re.match(r'^[a-zA-Z\s-]+$', v):
                raise ValueError('Full name can only contain letters, spaces, and hyphens')
            return v.strip()
        return v

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "full_name": "John William Doe",
                "role": "user",
                "disabled": False
            }
        }

