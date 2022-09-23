import uuid

from database import session

from sqlalchemy import Column, Enum, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID

from database import Model


class Status:
    in_progress = 0
    cancelled = 1
    completed = 2


class Emergency(Model):
    __tablename__ = "emergencies"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    status = Column(Enum(Status), default=Status.in_progress)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)

    @staticmethod
    def get(emergency_id: uuid.UUID):
        return session.query(Emergency).get(emergency_id)

    @staticmethod
    def create(emergency):
        session.add(
            Emergency(
                id=uuid.uuid4(),
                status=emergency.status,
                latitude=emergency.latitude,
                longitude=emergency.longitude,
                created_at=datetime.datetime.utcnow()
            )
        )
        session.commit()

    @staticmethod
    def update(emergency):
        session.query(Emergency).filter(Emergency.id == emergency.id).update(
            Emergency(
                status=emergency.status,
                latitude=emergency.latitude,
                longitude=emergency.longitude,
                closed_at=emergency.closed_at
            )
        )
        session.commit()

    @staticmethod
    def delete(emergency_id: uuid.UUID):
        session.query(Emergency).filter(Emergency.id == emergency_id).delete()
        session.commit()
