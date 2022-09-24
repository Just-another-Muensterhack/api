from uuid import UUID

from pydantic import BaseModel


class UuidRequest(BaseModel):
    uuid: UUID


class UuidResponse(BaseModel):
    uuid: UUID


class SuccessResponse(BaseModel):
    success: bool
