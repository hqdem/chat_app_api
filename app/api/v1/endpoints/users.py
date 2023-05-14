from typing import List, Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.crud_user import crud_user
from app.schemas.user import User, UserCreate

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
