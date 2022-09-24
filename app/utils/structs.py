from pydantic import BaseModel
from uuid import UUID

# requests


class UuidRequest(BaseModel):
    uuid: UUID


# responses


class UuidResponse(BaseModel):
    uuid: UUID


class SuccessResponse(BaseModel):
    success: bool
