from .jwt import Token, get_current_user
from .structs import SuccessResponse, UuidResponse

from schema.user import User
from schema.emergency import Status

from typing import Union, List
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

emergency_router = APIRouter(prefix="/emergency")


class UpdateEmergency(BaseModel):
    status: Status


# does not require auth
@emergency_router.get("/create", response_model=UuidResponse)
async def user_create(current_user: User = Depends(get_current_user)):
    """
    creates an emergency
    """
    return {"id": "random uuid"}


@emergency_router.post("/update", response_model=SuccessResponse)
async def user_create(current_user: User = Depends(get_current_user)):
    """
    updates the status of an emergency
    """
    return {"success": True}


@emergency_router.get("/terminate", response_model=SuccessResponse)
async def user_create(current_user: User = Depends(get_current_user)):
    """
    termiantes the emergency
    """
    return {"success": True}


@emergency_router.get("/terminate", response_model=SuccessResponse)
async def user_create(current_user: User = Depends(get_current_user)):
    """
    termiantes the emergency
    """
    return {"success": True}
