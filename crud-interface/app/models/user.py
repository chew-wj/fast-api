from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime, timedelta



class User(BaseModel):
    name: str
    email: EmailStr
    full_name: Optional[str] = None
    hashed_password: Optional[str] = None
    disabled: bool = False
    role: str = "user"  # Can be "user" or "admin"
    created_at: datetime = Field(default_factory=datetime.utcnow)

