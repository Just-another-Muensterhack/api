from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class TokenData(BaseModel):
    user_id: Optional[UUID]


class Token(BaseModel):
    access_token: str
    token_type: str
