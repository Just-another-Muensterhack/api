from uuid import uuid4, UUID
from enum import Enum
from datetime import datetime

from database import session, Base

from sqlalchemy import Column, Enum as EnumColumn, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ValidationError, validator

from database import Base, session


class Status(Enum):
    IN_PROGRESS = 0
    CANCELLED = 1
    COMPLETED = 2


class Emergency(Base):
    __tablename__ = "emergency"

    uuid = Column(UUIDColumn(as_uuid=True), primary_key=True, index=True, default=uuid4)
    status = Column(EnumColumn(Status), nullable=False, default=Status.IN_PROGRESS)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class EmergencyBase(BaseModel):
    uuid: UUID
    status: Status
    latitude: float
    longitude: float
    created_at: datetime

    class Config:
        orm_mode = True


class EmergencyCreate(BaseModel):
    device: UUID


class EmergencyUpdate(BaseModel):
    status: Status


class EmergencyList(BaseModel):
    emergencies: list[EmergencyBase]


class EmergencyLog(BaseModel):
    emergency: UUID


class QuestionModel(Base):
    __tablename__ = "question"

    uuid = Column(UUIDColumn(as_uuid=True), primary_key=True, index=True, default=uuid4)

    emergency_uuid = Column(UUIDColumn(as_uuid=True), ForeignKey("emergency.uuid", ondelete="CASCADE"))
    emergency = relationship("Emergency", foreign_keys=[emergency_uuid], passive_deletes=True)

    question_tag = Column(String(64))
    anwer_tag = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)


# questions answered by the patient to help the rescuers
class Question(BaseModel):
    question: str
    answer: str
    time: datetime
    hints: list[str]


class QuestionBulk(BaseModel):
    questions: list[Question]
