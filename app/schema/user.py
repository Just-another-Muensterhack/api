import datetime
import enum
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..db import Base


class Role(enum.Enum):
    admin = 0
    support = 1
    user = 2


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
