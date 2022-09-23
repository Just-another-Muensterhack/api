import enum

from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

from .emergencies import Emergencies
from .users import Users
from ..db import Base


class Type(enum.Enum):
    patient = 0
    aide = 1


class EmergencyUsers(Base):
    __tablename__ = "emergency_users"

    user_id = relationship(Users.id)
    emergency_id = relationship(Emergencies.id)
    type = Column(Enum(Type), nullable=False)
