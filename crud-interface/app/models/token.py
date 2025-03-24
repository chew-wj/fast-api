from pydantic import BaseModel,Field
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime, timedelta



# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None