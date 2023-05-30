from typing import Annotated, List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.crud.crud_chat import crud_chat
from app.crud.crud_message import crud_message
from app.models.user import User
from app.schemas.messages import Message, MessageCreate

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[Message], dependencies=[Depends(get_current_user)])
async def get_all_messages(db: Annotated[Session, Depends(get_db)],
                     skip: int = 0, limit: int = 100):
    # TODO: add permissions
    return crud_message.get_multi(db, skip=skip, limit=limit)


@router.post('/{chat_id}', status_code=status.HTTP_201_CREATED, response_model=Message)
async def create_message(db: Annotated[Session, Depends(get_db)], chat_id: int, user: Annotated[User, Depends(get_current_user)],
                   message_data: MessageCreate):
    # TODO: optimise query
    chat = crud_chat.get_one(db, id=chat_id)
    if chat is None:
        raise HTTPException(detail='Chat with that id not found', status_code=status.HTTP_404_NOT_FOUND)
    if user != chat.owner and user not in chat.users:
        raise HTTPException(detail='Permission denied', status_code=status.HTTP_403_FORBIDDEN)
    obj_in = dict(**message_data.dict(), chat_id=chat.id, sender_id=user.id)
    return crud_message.create(db, obj_in=obj_in)
