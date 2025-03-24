from pydantic import BaseModel,Field
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime, timedelta



class User(BaseModel):
    name: str
    email: str
    full_name: Optional[str] = None

class UserCreate(User):
    password: str

