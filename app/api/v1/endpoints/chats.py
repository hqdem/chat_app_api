from typing import Annotated, List

from fastapi import APIRouter, Depends, WebSocket, WebSocketException, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.api.v1.utils.websockets import ConnectionManager
from app.schemas.chat import Chat, ChatCreate, ChatUpdate
from app.schemas.user import User, UserBase
from app.crud.crud_chat import crud_chat

router = APIRouter()


@router.websocket('/ws_chat')
async def start_chat(db: Annotated[Session, Depends(get_db)],
                     manager: Annotated[ConnectionManager, Depends(ConnectionManager)], websocket: WebSocket):
    await manager.connect(websocket)
    creds_data = await websocket.receive_text()

    try:
        await manager.authenticate_user(db, creds_data, websocket)
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Message text was: {data}", websocket)
    except WebSocketException as ex:
        await manager.disconnect(websocket, code=ex.code, reason=ex.reason)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[Chat], dependencies=[Depends(get_current_user)])
async def get_chats(db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 100):
    return crud_chat.get_multi(db, skip=skip, limit=limit)


@router.get('/my', status_code=status.HTTP_200_OK, response_model=List[Chat])
async def get_chats_by_owner(db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)],
                             skip: int = 0, limit: int = 100):
    return crud_chat.get_multi_by_owner(db, owner=user, skip=skip, limit=limit)


@router.get('/{chat_id}', status_code=status.HTTP_200_OK, response_model=Chat, dependencies=[Depends(get_current_user)])
async def get_chat(db: Annotated[Session, Depends(get_db)], chat_id: int):
    chat = crud_chat.get_one(db, id=chat_id)
    if chat is None:
        raise HTTPException(detail='Chat not found', status_code=status.HTTP_404_NOT_FOUND)
    return chat


@router.get('/{chat_id}/get_users', status_code=status.HTTP_200_OK, response_model=List[User])
async def get_chat_users(db: Annotated[Session, Depends(get_db)], chat_id: int,
                         user: Annotated[User, Depends(get_current_user)], skip: int = 0, limit: int = 100):
    chat = crud_chat.get_one(db, id=chat_id)
    if chat is None:
        raise HTTPException(detail='Chat not found', status_code=status.HTTP_404_NOT_FOUND)
    if chat.owner != user:
        raise HTTPException(detail='Permission denied', status_code=status.HTTP_403_FORBIDDEN)
    return crud_chat.get_chat_users(chat=chat)


@router.post('/{chat_id}/add_users', status_code=status.HTTP_204_NO_CONTENT)
async def add_chat_users(db: Annotated[Session, Depends(get_db)], chat_id: int, user: Annotated[User, Depends(get_current_user)],
                         add_users: List[UserBase]):
    chat = crud_chat.get_one(db, id=chat_id)
    if chat is None:
        raise HTTPException(detail='Chat not found', status_code=status.HTTP_404_NOT_FOUND)
    if chat.owner != user:
        raise HTTPException(detail='Permission denied', status_code=status.HTTP_403_FORBIDDEN)
    crud_chat.add_users_to_chat(db, chat=chat, users=add_users)


@router.delete('/{chat_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(db: Annotated[Session, Depends(get_db)], chat_id: int,
                      user: Annotated[User, Depends(get_current_user)]):
    chat = crud_chat.get_one(db, id=chat_id)
    if chat is None:
        raise HTTPException(detail='Chat not found', status_code=status.HTTP_404_NOT_FOUND)
    if chat.owner != user:
        raise HTTPException(detail='Permission denied', status_code=status.HTTP_403_FORBIDDEN)
    crud_chat.delete(db, id=chat_id)


@router.put('/{chat_id}', status_code=status.HTTP_200_OK, response_model=Chat)
async def update_chat(db: Annotated[Session, Depends(get_db)], chat_id: int,
                      user: Annotated[User, Depends(get_current_user)], chat_update: ChatUpdate):
    chat = crud_chat.get_one(db, id=chat_id)
    if chat is None:
        raise HTTPException(detail='Chat not found', status_code=status.HTTP_404_NOT_FOUND)
    if chat.owner != user:
        raise HTTPException(detail='Permission denied', status_code=status.HTTP_403_FORBIDDEN)
    crud_chat.update(db, db_obj=chat, obj_in=chat_update)
    return chat


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Chat)
async def create_chat(db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)],
                      chat: ChatCreate):
    chat_obj_in = {**chat.dict()}
    chat_obj = crud_chat.create(db, obj_in=chat_obj_in)
    crud_chat.add_owner(db, chat_obj, user)
    return chat_obj
