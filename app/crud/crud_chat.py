from typing import List

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.crud.crud_user import crud_user
from app.models.message import Message
from app.models.user import User
from app.schemas.chat import ChatUpdate, ChatCreate
from app.models.chat import Chat
from app.schemas.user import UserBase


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Chat]:
        return db.query(self.model).options(joinedload(Chat.owner)).offset(skip).limit(
            limit).all()

    def get_multi_by_owner(self, db: Session, *, owner: User, skip: int = 0, limit: int = 100) -> List[Chat]:
        return db.query(self.model).options(joinedload(Chat.owner)).filter(Chat.owner == owner).offset(skip).limit(
            limit).all()

    def get_all_user_chats(self, db: Session, *, user: User, skip: int = 0, limit: int = 100) -> List[Chat]:
        return db.query(self.model).options(joinedload(Chat.owner).joinedload(User.chats)).filter(
            or_(Chat.owner == user, Chat.users.contains(user))).offset(
            skip).limit(limit).all()

    def add_owner(self, db: Session, chat: Chat, owner: User) -> None:
        chat.owner = owner
        db.add(chat)
        db.commit()
        db.refresh(chat)

    def get_chat_users(self, chat: Chat) -> List[User]:
        return chat.users

    def add_users_to_chat(self, db: Session, chat: Chat, users: List[UserBase]) -> None:
        db_users = crud_user.get_users_by_logins(db, users)
        for db_user in db_users:
            chat.users.append(db_user)
        db.add(chat)
        db.commit()
        db.refresh(chat)

    def get_messages_history(self, chat: Chat) -> List[Message]:
        # TODO: optimise queries
        return chat.messages


crud_chat = CRUDChat(Chat)
