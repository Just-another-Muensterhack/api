from datetime import datetime
import uuid

import enum
from sqlalchemy import Column, Enum, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class Status(enum.Enum):
    in_progress = 0
    cancelled = 1
    completed = 2


class Emergency(Base):
    __tablename__ = "emergency"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    status: Status = Column(Enum(Status), default=Status.in_progress)
    start: datetime = Column(DateTime, default=datetime.utcnow)
    end: datetime = Column(DateTime, nullable=True)
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)

