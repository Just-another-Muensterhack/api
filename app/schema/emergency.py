import datetime
import uuid

from sqlalchemy import Column, Enum, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class Status:
    in_progress = 0
    cancelled = 1
    completed = 2


class Emergencie(Base):
    __tablename__ = "emergencies"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    status = Column(Enum(Status), default=Status.in_progress)
    start = Column(DateTime, default=datetime.datetime.utcnow)
    end = Column(DateTime, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
