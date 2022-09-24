import os
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from database import session
from models.security import TokenData
from models.user import User


def get_secret_key() -> str:
    return os.getenv("JWT_SECRET", default="A" * 32)


SECRET_KEY: str = get_secret_key()
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS: int = 30
TOKEN_EXPIRATION_DAYS: int = 365
pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")


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

        user_id: str = payload.get("user")
        created_at: str = payload.get("created_at")

        if not user_id:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    # get actuall user struct from database
    user = session.query(User.uuid).filter_by(uuid=user_id).first()

    if not user:
        raise credentials_exception

    return user


def create_access_token(uuid: UUID):
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRATION_DAYS)

    to_encode = {
        "user": str(uuid),
        "created_at": datetime.utcnow().isoformat(),
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
