from enum import Enum
import uuid

from sqlalchemy import Column, Enum as EnumColumn, DateTime
from sqlalchemy.orm import relationship

from emergency import Emergency
from user import User
import datetime

from database import session, base


class Type(Enum):
    PATIENT = 0
    AIDE = 1


class EmergencyUser(base):
    __tablename__ = "emergency_user"

    user_uuid = Column(UUIDColumn(as_uuid=True), ForeignKey("user.uuid", ondelete="CASCADE"))
    emergency_uuid = Column(UUIDColumn(as_uuid=True), ForeignKey("emergency.uuid", ondelete="CASCADE"))

    user_type = Column(EnumColumn(Type), nullable=False, default=Type.PATIENT)

    user = relationship("User", foreign_keys=[user_uuid], passive_deletes=True)
    emergency = relationship("Emergency", foreign_keys=[emergency_uuid], passive_deletes=True)
