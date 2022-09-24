from pydantic import BaseModel
from uuid import UUID


class UuidRequest(BaseModel):
    uuid: UUID


class UuidResponse(BaseModel):
    uuid: UUID


class SuccessResponse(BaseModel):
    success: bool


class DeviceUpdateCoordinates(BaseModel):
    device: UUID
    latitude: float
    longitude: float
