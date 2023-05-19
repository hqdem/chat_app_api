from typing import List

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.chat import ChatUpdate, ChatCreate
from app.models.chat import Chat


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 0) -> List[Chat]:
        return db.query(self.model).options(joinedload(Chat.owner)).offset(skip).limit(limit).all()

    def add_owner(self, db: Session, chat: Chat, owner: User) -> None:
        chat.owner = owner
        db.add(chat)
        db.commit()
        db.refresh(chat)


crud_chat = CRUDChat(Chat)
