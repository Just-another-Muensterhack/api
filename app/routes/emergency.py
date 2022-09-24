from utils.jwt import get_current_user

from models.user import User
from models.emergency import Status, Emergency, EmergencyCreate, EmergencyBase, EmergencyList, Question, QuestionBulk, EmergencyRead, EmergencyUpdateCoordinates
from models.helper import SuccessResponse, UuidResponse, UuidRequest
from models.security import Token

from uuid import UUID, uuid4
from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

emergency_router = APIRouter(prefix="/emergency")

# does not require auth
@emergency_router.post("/create", response_model=UuidResponse)
async def emergency_create(request: EmergencyCreate, current_user: User = Depends(get_current_user)):
    """
    creates an emergency and taking the coordinates from specified device
    """

    device: Device = Device.query.get(request.device)
    emergency: Emergency = Emergency(device = device.uuid)

    session.add(emergency)
    session.commt()
    session.refresh()

    return {"id": emergency.uuid }


@emergency_router.delete("/terminate", response_model=SuccessResponse)
async def emergency_terminate(request: , current_user: User = Depends(get_current_user)):
    """
    termiantes the emergency
    """

    emergency = Emergency.query.get(uuid=request.device_uuid)

    if not emergency:
        return { "success": False }

    session.delete(emergency)
    session.commit()

    return {"success": True}


@emergency_router.put("/info", response_model=EmergencyList | SuccessResponse)
async def emergency_update(request: EmergencyRead, current_user: User = Depends(get_current_user)):
    """
    getting information about emergency
    """

    emergency = Emergency.query.get(uuid=request.device)

    if not emergency:
        return {"success": False}

    return emergency


@emergency_router.put("/coordinates", response_model=SuccessResponse)
async def emergency_coordinates(coordinates: EmergencyUpdateCoordinates, current_user: User = Depends(get_current_user)):
    """
    receiving coordinates of the accident
    """

    emergency = Emergency.query.get(uuid=request.;)

    if not device:
        return {"success": False}

    device.latitude = request.lat
    device.longitude = request.lon

    session.commit()


    return {"success": True}


@emergency_router.post("/accept", response_model=SuccessResponse)
async def emergency_accept(current_user: User = Depends(get_current_user)):
    """
    accept helping
    """
    return {"success": True}


@emergency_router.post("/deny", response_model=SuccessResponse)
async def emergency_deny(current_user: User = Depends(get_current_user)):
    """
    deny helping
    """
    return {"success": True}


@emergency_router.put("/log/single", response_model=SuccessResponse)
async def emergency_log_single(log: Question, current_user: User = Depends(get_current_user)):
    """
    setting one question
    """
    return {"success": True}


@emergency_router.put("/log/bulk", response_model=SuccessResponse)
async def emersgency_log_bulk(log: QuestionBulk, current_user: User = Depends(get_current_user)):
    """
    setting multiple questions
    """
    return {"success": True}


@emergency_router.get("/log", response_model=QuestionBulk)
async def emergency_log_info(current_user: User = Depends(get_current_user)):
    """
    setting multiple questions
    """
    return {"questions": []}
