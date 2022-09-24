import enum
import uuid

from sqlalchemy import Column, Enum, DateTime
from sqlalchemy.orm import relationship

from emergency import Emergency
from user import User
from database import Model
import datetime
from database import session


class Type(enum.Enum):
    patient = 0
    aide = 1


class EmergencyUser(Model):
    __tablename__ = "emergency_users"

    user_id = relationship(User.id)
    emergency_id = relationship(Emergency.id)
    type = Column(Enum(Type), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def get(emergency_user_id: uuid.UUID):
        return session.query(EmergencyUser).get(emergency_user_id)

    @staticmethod
    def create(emergency_user):
        session.add(
            EmergencyUser(
                id=uuid.uuid4(),
                emergency_id=emergency_user.emergency_id,
                type=emergency_user.type,
                created_at=datetime.datetime.utcnow(),
            )
        )
        session.commit()

    @staticmethod
    def update(emergency_user):
        session.query(EmergencyUser).filter(Emergency.id == emergency_user.id).update(
            EmergencyUser(
                emergency_id=emergency_user.emergency_id,
            )
        )
        session.commit()

    @staticmethod
    def delete(emergency_user_id: uuid.UUID):
        session.query(EmergencyUser).filter(EmergencyUser.id == emergency_user_id).delete()
        session.commit()
