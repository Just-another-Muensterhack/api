from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from database import Model
from database import session


class Role(enum.Enum):
    admin = 0
    support = 1
    user = 2


class RegisteredUser(Model):
    __tablename__ = "registered_users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    phone_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(Role), default=Role.user)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    hashed_password = Column(String, nullable=True)

    @staticmethod
    def get(user_id: uuid.UUID):
        return session.query(User).get(user_id)

    @staticmethod
    def create():
        session.add(
            RegisteredUser(id=uuid.uuid4(), created_at=datetime.datetime.utcnow())
        )
        session.commit()

    @staticmethod
    def delete(user_id: uuid.UUID):
        session.query(User).filter(User.id == user_id).delete()
        session.commit()
