from utils.jwt import get_current_user, create_access_token

from models.user import session, User, UserDelete, UserRegister, UserLogin, UserRead
from models.device import DeviceDelete, DeviceUpdatePosition, DevicesList
from models.security import Token
from models.helper import SuccessResponse, UuidResponse, UuidRequest

from typing import Optional
from uuid import UUID, uuid4

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

user_router = APIRouter(prefix="/user")

# does not require auth
@user_router.post("/create", response_model=Token)
async def user_create():
    """
    creates basic user and returnes basic id from the user
    """

    user: User = User()

    session.add(user)
    session.commit()
    session.refresh(user)

    access_token = create_access_token(user.uuid)

    return {"access_token": str(access_token), "token_type": "bearer"}


@user_router.delete("/delete", response_model=SuccessResponse)
async def user_delete(request: UserDelete):
    """
    deletes requested user
    """

    user = User.query.get(uuid=request.user_uuid)

    if not user:
        return {"success": False}

    session.delete(user)
    session.commit()

    return {"success": True}


@user_router.post("/info", response_model=UserRead)
async def user_read(current_user: User = Depends(get_current_user)):
    """
    changes role of user to specified
    """

    return current_user


@user_router.put("/device", response_model=UuidResponse)
async def user_device_create(current_user: User = Depends(get_current_user)):
    """
    adds a new device to a user
    """

    device = Device(user_uuid=current_user.uuid)

    session.add(device)
    session.commit()
    session.refresh(device)

    return {"uuid": device.uuid}


@user_router.delete("/device", response_model=SuccessResponse)
async def user_device_delete(request: DeviceDelete, current_user: User = Depends(get_current_user)):
    """
    removes device from user
    """

    device = Device.query.get(uuid=request.uuid)

    if not device:
        return {"success": False}

    session.delete(device)
    session.commit()

    return {"success": True}


@user_router.post("/device/update", response_model=SuccessResponse)
async def user_device_update_position(request: DeviceUpdatePosition, current_user: User = Depends(get_current_user)):
    """
    updates the position of specified device
    """

    device = Device.query.get(uuid=request.uuid)

    if not device:
        return {"success": False}

    device.latitude = request.lat
    device.longitude = request.lon

    session.commit()

    return {"success": True}


@user_router.post("/device/list", response_model=DevicesList)
async def user_device_read(current_user: User = Depends(get_current_user)):
    """
    list all devices belonging to this user
    """

    return {"devices": session.query(Device.uuid).filter_by(user_uuid=current_user.uuid).all()}
