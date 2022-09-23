import enum

from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

from emergency import Emergencie
from user import User
from database import Model


class Type(enum.Enum):
    patient = 0
    aide = 1


class EmergencyUser(Model):
    __tablename__ = "emergency_users"

    user_id = relationship(User.id)
    emergency_id = relationship(Emergencie.id)
    type = Column(Enum(Type), nullable=False)
