from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from database import Base, session


class User(Base):
    __tablename__ = "user"

    uuid = Column(UUIDColumn(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)

    devices = relationship("Device", back_populates="user", passive_deletes=True)


class UserDelete(BaseModel):
    user_uuid: UUID


class UserRegister(BaseModel):
    user_uuid: UUID
    phone: str
    password: str
    first_name: str
    second_name: str


class UserLogin(BaseModel):
    email: str
    password_hash: str


class UserRead(BaseModel):
    uuid: UUID
    email: Optional[str]
    role: Optional[int]
