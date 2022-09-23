from .jwt import Token, get_current_user
from .structs import SuccessResponse, UuidResponse

from schema.user import User

from typing import Union, List
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

user_router = APIRouter(prefix="/users")


class User:
    id: UUID


# Request Types
class UserDelete(BaseModel):
    user_id: UUID


class UserRegister(BaseModel):
    user_id: UUID
    phone: str
    password: str
    first_name: str
    second_name: str


class UserLogin(BaseModel):
    email: str
    password_hash: str


class PromoteUser(BaseModel):
    user_id: UUID
    role: int  # TODO: change to enum


class AddDevice(BaseModel):
    user_id: UUID
    token: str  # TODO: discuss


class RemoveDevice(BaseModel):
    device_id: UUID


class UpdatePosition(BaseModel):
    device_id: UUID
    lat: float
    lon: float


# Response Types


class SessionResponse(BaseModel):
    success: bool
    jwt: str


class DevicesList(BaseModel):
    devices: List[UUID]


# does not require auth
@user_router.post("/create", response_model=UuidResponse)
async def user_create():
    """
    creates basic user and returnes basic id from the user
    """
    return {"id": "random uuid"}


@user_router.delete("/delete", response_model=SuccessResponse)
async def user_delete(request: UserDelete):
    """
    deletes requested user
    """
    return {"id": "random uuid"}


# does not require auth
@user_router.post("/register", response_model=SuccessResponse)
async def user_register(request: UserRegister):
    """
    registeres user
    """
    return {"sucess": True}


@user_router.post("/login", response_model=Token)
async def user_register(request: OAuth2PasswordRequestForm = Depends()):
    """
    login user
    """
    return {"sucess": True, "jwt": "example"}


@user_router.post("/promote", response_model=SuccessResponse)
async def user_promote(request: PromoteUser, current_user: User = Depends(get_current_user)):
    """
    changes role of user to specified
    """

    return {"success": True}


@user_router.put("/device", response_model=UuidResponse)
async def user_device_add(request: AddDevice, current_user: User = Depends(get_current_user)):
    """
    adds a new device to a user
    """

    return {"id": "random uuid"}


@user_router.delete("/device", response_model=SuccessResponse)
async def user_device_remove(request: RemoveDevice, current_user: User = Depends(get_current_user)):

    """
    removes device from user
    """

    return {"success": True}


@user_router.post("/device/update", response_model=SuccessResponse)
async def user_device_remove(request: UpdatePosition, current_user: User = Depends(get_current_user)):

    """
    updates the position of specified device
    """

    return {"success": True}


@user_router.post("/device/list", response_model=DevicesList)
async def user_promote(request: PromoteUser, current_user: User = Depends(get_current_user)):

    """
    list all devices belonging to this user
    """

    return {"devices": []}
