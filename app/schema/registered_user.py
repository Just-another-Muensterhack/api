from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from datetime import datetime
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
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def get(user_id: uuid.UUID):
        return session.query(RegisteredUser).get(user_id)

    @staticmethod
    def create(user):
        session.add(
            RegisteredUser(
                id=uuid.uuid4(),
                phone_number=user.phone_number,
                email=user.email,
                role=Role.user,
                first_name=user.first_name,
                last_name=user.last_name,
                hashed_password=user.hashed_password,
                created_at=datetime.utcnow(),
            )
        )
        session.commit()

    @staticmethod
    def update(user):
        existing_user = session.query(RegisteredUser).filter(
            RegisteredUser.id == user.id
        )
        existing_user.update(
            {
                RegisteredUser.phone_number: user.phone_number,
                RegisteredUser.email: user.email,
                RegisteredUser.role: user.role,
                RegisteredUser.first_name: user.first_name,
                RegisteredUser.last_name: user.last_name,
                RegisteredUser.hashed_password: user.hashed_password,
            }
        )
        session.commit()

    @staticmethod
    def delete(user_id: uuid.UUID):
        session.query(RegisteredUser).filter(RegisteredUser.id == user_id).delete()
        session.commit()
