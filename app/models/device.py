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

    def __repr__(self):
        return "<Device {name} ({lat}, {lon})>".format(name=self.location, lat=self.latitude, lon=self.longitude)

    def get_devices_within_radius(self, radius):
        """Return all devices within a given radius (in meters) of this device."""

        devices = session.query(Device.uuid).filter(func.ST_DistanceSphere(Device.geo, self.geo) < radius).all()
        return devices

    @classmethod
    def add_device(cls, location, longitude, latitude):
        """Put a new device in the database."""

        geo = "POINT({} {})".format(longitude, latitude)
        device = Device(longitude=longitude, latitude=latitude, geo=geo)

        session.add(device)
        session.commit()

    @classmethod
    def update_geometries(cls):
        """Using each device's longitude and latitude, add geometry data to db."""

        devices = Device.query.all()

        for device in devices:
            point = "POINT({} {})".format(device.longitude, device.latitude)
            device.geo = point

        session.commit()


class DeviceDelete(BaseModel):
    device_uuid: UUID


class DeviceUpdatePosition(BaseModel):
    device_uuid: UUID
    lat: float
    lon: float


class DevicesList(BaseModel):
    devices: list[UUID]
