from uuid import uuid4, UUID
from enum import Enum
from datetime import datetime

from database import session

from sqlalchemy import Column, Enum, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn

from database import Model


class Status(Enum):
    IN_PROGRESS = 0
    CANCELLED = 1
    COMPLETED = 2


class Emergency(Model):
    __tablename__ = "emergency"

    uuid = Column(UUIDColumn(as_uuid=True), primary_key=True, index=True, default=uuid4)
    status = Column(Enum(Status), nullable=False, default=Status.IN_PROGRESS)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
