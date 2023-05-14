from typing import Generator, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.crud_user import crud_user
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenPayload


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(db: Annotated[Session, Depends(get_db)], token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]) -> User:
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(detail="Couldn't validate credentials", status_code=status.HTTP_401_UNAUTHORIZED)
    user = crud_user.get_user_by_login(db, login=token_data.sub)
    if not user:
        raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)
    return user
