import datetime
from datetime import timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.token import TokenPayload

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(sub: str, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.datetime.now() + expires_delta
    else:
        expire = datetime.datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    encode_data = {
        'sub': sub,
        'exp': expire
    }
    encoded_jwt = jwt.encode(encode_data, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt
