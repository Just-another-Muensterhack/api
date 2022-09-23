import uuid
import datetime
from sqlalchemy import Column, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from user import User
from database import Model
from database import session


class Device(Model):
    __tablename__ = "devices"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id: UUID = relationship(User.id)
    latitude: float = Column(Float, nullable=False)
    longitude: float = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def get(device_id: uuid.UUID):
        return session.query(Device).get(device_id)

    @staticmethod
    def create(device):
        session.add(
            Device(
                id=uuid.uuid4(),
                user_id=device.user_id,
                latitude=device.latitude,
                longitude=device.longitude,
                created_at=datetime.datetime.utcnow(),
            )
        )
        session.commit()

    @staticmethod
    def update(device):
        session.query(Device).filter(Device.id == device.id).update(
            Device(latitude=device.latitude, longitude=device.longitude)
        )
        session.commit()

    @staticmethod
    def delete(device_id: uuid.UUID):
        session.query(Device).filter(Device.id == device_id).delete()
        session.commit()
