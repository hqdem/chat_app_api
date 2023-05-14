from typing import List, Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import create_access_token
from app.crud.crud_user import crud_user
from app.schemas.token import Token
from app.schemas.user import User, UserCreate, UserCredentials

router = APIRouter()


@router.get('/', response_model=List[User], status_code=status.HTTP_200_OK)
def get_users(db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 100):
    return crud_user.get_multi(db, skip=skip, limit=limit)


@router.post('/register', response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(db: Annotated[Session, Depends(get_db)], user: UserCreate):
    try:
        user = crud_user.create(db, obj_in=user)
        return user
    except IntegrityError:
        raise HTTPException(detail='User with that login already exists', status_code=status.HTTP_409_CONFLICT)


@router.post('/authenticate', response_model=Token, status_code=status.HTTP_200_OK)
def auth_user(db: Annotated[Session, Depends(get_db)], creds: UserCredentials):
    user = crud_user.authenticate(db, login=creds.login, password=creds.password)
    if user is None:
        raise HTTPException(detail='Incorrect credentials', status_code=status.HTTP_401_UNAUTHORIZED)
    if user.is_active is False:
        raise HTTPException(detail='User is inactive', status_code=status.HTTP_400_BAD_REQUEST)

    return {
        'access_token': create_access_token(user.login),
        'token_type': 'Bearer'
    }
