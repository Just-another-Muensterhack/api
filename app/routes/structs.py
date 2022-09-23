from pydantic import BaseModel

# requests

class SuccessResponse(BaseModel):
    success: bool

# responses

class UuidResponse(BaseModel):
    id: UUID


