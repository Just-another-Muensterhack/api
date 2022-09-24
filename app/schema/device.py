from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy import Column, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from sqlalchemy.orm import relationship

from user import User
from database import Model
from database import session


class Device(Model):
    __tablename__ = "devices"

    uuid = Column(UUIDColumn(as_uuid=True), primary_key=True, index=True, default=uuid4)
    latitude = Column(Float, nullable=False, default=0)
    longitude = Column(Float, nullable=False, default=0)

    user_uuid = Column(UUIDColumn(as_uuid=True), Foreignkey("user.uuid", ondelete="CASCADE"))

    user = relationship("User", back_populates="devices", passive_deletes=True)

