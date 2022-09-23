from sqlalchemy import Column, String, Enum, Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from db import Base


class Role(enum.Enum):
    admin = 0
    support = 1
    user = 2


class RegisteredUser(Base):
    __tablename__ = "registered_users"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    phone_number: str = Column(String, unique=True, index=True)
    email: str = Column(String, unique=True, index=True)
    role: Role = Column(Enum(Role), default=Role.user)
    first_name: str = Column(String, index=True)
    last_name: str = Column(String, index=True)
    hashed_password: Optional[str] = Column(String, nullable=True)

