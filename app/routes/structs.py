from pydantic import BaseModel
from uuid import UUID

# requests


class SuccessResponse(BaseModel):
    success: bool


# responses


class UuidResponse(BaseModel):
    id: UUID
