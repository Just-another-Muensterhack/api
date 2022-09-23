from pydantic import BaseModel
from uuid import UUID

# requests


class UuidRequest(BaseModel):
    id: UUID


# responses


class UuidResponse(BaseModel):
    id: UUID


class SuccessResponse(BaseModel):
    success: bool
