from .jwt import Token, get_current_user
from .structs import SuccessResponse, UuidResponse

from schema.user import User
from schema.emergency import Status

from uuid import UUID, uuid4
from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

emergency_router = APIRouter(prefix="/emergency")


class CreateEmergency(BaseModel):
    device: UUID


class UpdateEmergency(BaseModel):
    status: Status


class UpdateSeverity(BaseModel):
    severity: int


class Question(BaseModel):
    question: str
    answer: str
    time: datetime


class BulkLog(BaseModel):
    questions: list[Question]


class EmergencyInfo(BaseModel):
    id: UUID
    lat: float
    lon: float
    severity: int


class EmergencyList(BaseModel):
    emergencies: list[EmergencyInfo]


# does not require auth
@emergency_router.post("/create", response_model=UuidResponse)
async def user_create(request: CreateEmergency):
    """
    creates an emergency and taking the coordinates from specified device
    """
    return {"id": uuid4()}


@emergency_router.post("/coordinates", response_model=SuccessResponse)
async def coordinates(current_user: User = Depends(get_current_user)):
    """
    updates the status of an emergency
    """
    return {"success": True}


@emergency_router.delete("/terminate", response_model=SuccessResponse)
async def emergency_terminate(current_user: User = Depends(get_current_user)):
    """
    termiantes the emergency
    """
    return {"success": True}


@emergency_router.put("/update", response_model=SuccessResponse)
async def emergency_update(current_user: User = Depends(get_current_user)):
    """
    setting severity
    """
    return {"success": True}


@emergency_router.put("/info", response_model=EmergencyInfo)
async def emergency_update(current_user: User = Depends(get_current_user)):
    """
    setting severity
    """
    return {"id": "uuid", "lat": 0, "lon": 0, "severity": 5}


@emergency_router.put("/log/single", response_model=SuccessResponse)
async def emergency_log_single(log: Question, current_user: User = Depends(get_current_user)):
    """
    setting one question
    """
    return {"success": True}


@emergency_router.put("/log/bulk", response_model=SuccessResponse)
async def emergency_log_single(log: BulkLog, current_user: User = Depends(get_current_user)):
    """
    setting multiple questions
    """
    return {"success": True}


@emergency_router.get("/log", response_model=BulkLog)
async def emergency_log_single(current_user: User = Depends(get_current_user)):
    """
    setting multiple questions
    """
    return {"questions": []}


@emergency_router.post("/accept", response_model=SuccessResponse)
async def emergency_log_single(current_user: User = Depends(get_current_user)):
    """
    accept helping
    """
    return {"success": True}


@emergency_router.post("/deny", response_model=SuccessResponse)
async def emergency_log_single(current_user: User = Depends(get_current_user)):
    """
    deny helping
    """
    return {"questions": True}


@emergency_router.post("/poll", response_model=EmergencyList)
async def emergency_log_single(current_user: User = Depends(get_current_user)):
    """
    actively poll for emergencies
    """
    return {"emergencies": []}
