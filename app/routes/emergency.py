from fastapi import Depends, APIRouter, HTTPException, status

from database import session
from models.device import Device
from models.emergency import Emergency, EmergencyCreate, EmergencyList, Question, QuestionBulk, EmergencyRead, \
    EmergencyDelete, Status, EmergencyUUID, EmergencyBase
from models.emergency_user import EmergencyUser
from models.helper import SuccessResponse, UuidResponse
from models.user import User
from utils.jwt import get_current_user

emergency_router = APIRouter(prefix="/emergency")


# does not require auth
@emergency_router.post("/create", response_model=UuidResponse)
async def emergency_create(request: EmergencyCreate, _: User = Depends(get_current_user)):
    """
    creates an emergency and taking the coordinates from specified device
    """

    device: Device = session.query(Device.uuid).filter_by(uuid=request.device).first()

    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    emergency: Emergency = Emergency(longitude=request.longitude, latitude=request.latitude)

    session.add(emergency)
    session.commit()
    session.refresh(emergency)

    return {"uuid": emergency.uuid}


@emergency_router.delete("/terminate", response_model=SuccessResponse)
async def emergency_terminate(request: EmergencyDelete, _: User = Depends(get_current_user)):
    """
    termiantes the emergency
    """

    emergency = Emergency.query.get(uuid=request.emergency)

    if not emergency:
        return {"success": False}

    emergency.status = Status.COMPLETED
    session.commit()

    return {"success": True}


@emergency_router.put("/info", response_model=EmergencyList)
async def emergency_read(request: EmergencyRead, _: User = Depends(get_current_user)):
    """
    getting information about emergency
    """

    emergency = Emergency.query.get(uuid=request.emergency)

    if not emergency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return emergency


@emergency_router.post("/accept", response_model=SuccessResponse)
async def emergency_accept(request: EmergencyUUID, current_user: User = Depends(get_current_user)):
    """
    accept helping
    """
    if not Emergency.query.get(uuid=request.uuid):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    emergency_user = EmergencyUser(user_uuid=current_user.uuid, emergency_uuid=request.uuid)

    session.add(emergency_user)
    session.commit()

    return {"success": True}


@emergency_router.post("/deny", response_model=SuccessResponse)
async def emergency_deny(_: EmergencyUUID, __: User = Depends(get_current_user)):
    """
    accept helping
    """

    return {"success": True}


@emergency_router.put("/log/single", response_model=SuccessResponse)
async def emergency_log_single(log: Question, current_user: User = Depends(get_current_user)):
    """
    setting one question
    """

    print(log.answer)
    return {"success": True}


@emergency_router.put("/log/bulk", response_model=SuccessResponse)
async def emersgency_log_bulk(log: QuestionBulk, current_user: User = Depends(get_current_user)):
    """
    setting multiple questions
    """
    print(log.questions)
    return {"success": True}


@emergency_router.get("/log", response_model=QuestionBulk)
async def emergency_log_info(current_user: User = Depends(get_current_user)):
    """
    setting multiple questions
    """
    return {"questions": []}


@emergency_router.get("/poll", response_model=EmergencyBase)
async def emergency_poll(_: User = Depends(get_current_user)):
    emergency = session.query(Emergency).first()

    if not emergency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return emergency
