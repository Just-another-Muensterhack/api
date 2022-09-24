import requests

from utils.jwt import get_current_user

from models.user import User
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
async def emergency_create(request: EmergencyCreate, current_user: User = Depends(get_current_user)):
    """
    creates an emergency and taking the coordinates from specified device
    """

    device: Device = Device.query.get(request.device)
    emergency: Emergency = Emergency(device=device.uuid)

    return {"id": uuid4()}


@emergency_router.delete("/terminate", response_model=SuccessResponse)
async def emergency_terminate(current_user: User = Depends(get_current_user)):
    """
    termiantes the emergency
    """
    return {"success": True}


@emergency_router.put("/info", response_model=EmergencyList)
async def emergency_update(current_user: User = Depends(get_current_user)):
    """
    setting severity
    """
    return {"uuid": "uuid", "latitude": 0, "longitude": 0, "severity": 5, "status": 1}


@emergency_router.put("/coordinates", response_model=SuccessResponse)
async def emergency_coordinates(coordinates: DeviceUpdateCoordinates, current_user: User = Depends(get_current_user)):
    """
    receiving coordinates of the accident
    """
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
