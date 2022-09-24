from enum import Enum
from uuid import uuid4

from sqlalchemy import Column, Enum as EnumColumn, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from sqlalchemy.orm import relationship

from database import Base


class Type(Enum):
    PATIENT = 0
    AIDE = 1


class EmergencyUser(Base):
    __tablename__ = "emergency_user"

    uuid = Column(UUIDColumn(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_uuid = Column(UUIDColumn(as_uuid=True), ForeignKey("user.uuid", ondelete="CASCADE"))
    emergency_uuid = Column(UUIDColumn(as_uuid=True), ForeignKey("emergency.uuid", ondelete="CASCADE"))

    user_type = Column(EnumColumn(Type), nullable=False, default=Type.PATIENT)

    user = relationship("User", foreign_keys=[user_uuid], passive_deletes=True)
    emergency = relationship("Emergency", foreign_keys=[emergency_uuid], passive_deletes=True)
