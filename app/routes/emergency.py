from fastapi import Depends, APIRouter, HTTPException, status

import requests

from utils.jwt import get_current_user

from database import session
from models.device import Device
from models.emergency import (
    Emergency,
    EmergencyCreate,
    EmergencyList,
    Question,
    QuestionBulk,
    EmergencyRead,
    EmergencyDelete,
    Status,
    EmergencyUUID,
    EmergencyBase,
)
from models.emergency_user import EmergencyUser, Type
from models.helper import SuccessResponse, UuidResponse
from models.user import User

emergency_router = APIRouter(prefix="/emergency")

from models.emergency import (
    Status,
    Emergency,
    EmergencyCreate,
    EmergencyBase,
    EmergencyList,
    Question,
    QuestionBulk,
    EmergencyLog,
)
from models.helper import SuccessResponse, UuidResponse, UuidRequest, DeviceUpdateCoordinates
from models.security import Token

from uuid import UUID, uuid4
from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

emergency_router = APIRouter(prefix="/emergency")

graph_data = requests.get("https://cdn.helpwave.de/graph.json").json()

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
    if not session.query(Emergency).get(uuid=request.uuid):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    emergency_user = EmergencyUser(user_uuid=current_user.uuid, emergency_uuid=request.uuid)

    session.add(emergency_user)
    session.commit()

    return {"success": True}


@emergency_router.post("/deny", response_model=SuccessResponse)
async def emergency_deny(request: EmergencyUUID, current_user: User = Depends(get_current_user)):
    """
    deny helping
    """
    if not session.query(Emergency).get(uuid=request.uuid):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    emergency_user = EmergencyUser(user_uuid=current_user.uuid, emergency_uuid=request.uuid, type=Type.NONE)

    session.add(emergency_user)
    session.commit()

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


@emergency_router.get("/poll", response_model=EmergencyBase)
async def emergency_poll(_: User = Depends(get_current_user)):
    emergency = session.query(Emergency).first()

    if not emergency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return emergency


async def emergency_log_info(request: EmergencyLog, current_user: User = Depends(get_current_user)):
    """
    returns a list of all questions the patient answered before the first responder arrived
    """

    def _lookup(tag: str, lang: str = "de") -> str:
        # TODO don't we have a local copy of the graph.json anywhere in the repository?!
        return graph_data.get("language").get(lang).get(tag)

    def _get_hints(tag: str, lang: str = "de") -> list[str]:
        ret = []
        # TODO don't we have a local copy of the graph.json anywhere in the repository?!
        # grab all possibles responses and append all possible answers from the patient (=hints) to the list
        responses = graph_data.get("nodes").get(tag).get("responses")
        for resp in responses:
            ret.append(_lookup(resp.get("hint"), lang))
        return ret

    return [
        {
            "question": _lookup(e.question_tag),
            "answer": _lookup(e.answer_tag),
            "time": e.created_at,
            "hints": _get_hints(e.question_tag),
        }
        for e in session.query(Question.uuid).filter_by(emergency=request.emergency).all()
    ]
