from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn

from database import Model
from database import session


class User(Model):
    __tablename__ = "user"

    uuid = Column(UUIDColumn(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)

    devices = relationship("Device", back_populates="user", passive_deletes=True)
