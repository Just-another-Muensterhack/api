from datetime import datetime
import enum
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

from database import Model
from database import session


class Role(enum.Enum):
    admin = 0
    support = 1
    user = 2


class User(Model):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def get(user_id: uuid.UUID) -> 'User':
        # not sure if this throws something or just returnes NOne
        return session.query(User).get(user_id)

    @staticmethod
    def create() -> 'User':
        session.add(User(id=uuid.uuid4(), created_at=datetime.utcnow()))
        session.commit()

    @staticmethod
    def delete(user_id: uuid.UUID) -> bool:
        try:
            session.query(User).filter(User.id == user_id).delete()
            session.commit()
            return True
        except:
            return False

