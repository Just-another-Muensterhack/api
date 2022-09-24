from pydantic import BaseModel
from uuid import UUID


class UuidRequest(BaseModel):
    uuid: UUID


class UuidResponse(BaseModel):
    uuid: UUID


class SuccessResponse(BaseModel):
    success: bool

