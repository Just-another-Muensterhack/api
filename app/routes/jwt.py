from typing import Optional
from uuid import UUID
import os
import binascii
import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel


def generare_secret_key() -> str:
    binascii.b2a_hex(os.urandom(32))


def get_secret_key() -> str:
    # this sets a default value for the SECRET_KEY_FILE
    env_file_path: Optional[str] = os.getenv("SECRET_KEY_FILE")
    if not env_file_path:
        logging.warn("generating temporary secret key")
        return generare_secret_key()

    with open(env_file_path) as f:
        return f.read()


SECRET_KEY: str = get_secret_key()
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS: int = 30
pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    user_id: Optional[UUID]


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    # get actuall user struct from database
    # user = get_user(fake_users_db, user_id=token_data.user_id)

    if not user:
        raise credentials_exception
    return user
