from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from sqlalchemy import func
from geoalchemy2 import Geometry

from models.user import User
from database import Base, session


class Device(Base):
    __tablename__ = "devices"

    uuid = Column(UUIDColumn(as_uuid=True), primary_key=True, index=True, default=uuid4)
    latitude = Column(Float, nullable=False, default=0)
    longitude = Column(Float, nullable=False, default=0)
    geo = Column(Geometry(geometry_type="POINT"))

    user_uuid = Column(UUIDColumn(as_uuid=True), ForeignKey("user.uuid", ondelete="CASCADE"))

    user = relationship("User", back_populates="devices", passive_deletes=True)

    @staticmethod
    def get_devices_within_radius(self, radius):
        """Return all devices within a given radius (in meters) of this device."""

        return Device.query.filter(func.ST_Distance_Sphere(Device.geo, self.geo) < radius).all()


class DeviceDelete(BaseModel):
    device_uuid: UUID


class DeviceUpdatePosition(BaseModel):
    device_uuid: UUID
    lat: float
    lon: float


class DevicesList(BaseModel):
    devices: list[UUID]
