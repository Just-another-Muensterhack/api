import enum

from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

from emergency import Emergencie
from user import User
from db import Base


class Type(enum.Enum):
    patient = 0
    aide = 1


class EmergencyUser(Base):
    __tablename__ = "emergency_users"

    user_id: UUID = relationship(User.id)
    emergency_id: UUID = relationship(Emergencie.id)
    type: Type = Column(Enum(Type), nullable=False)
