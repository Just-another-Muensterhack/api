import uuid

from sqlalchemy import Column, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from user import User
from database import Model


class Device(Model):
    __tablename__ = "devices"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id: UUID = relationship(User.id)
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)
