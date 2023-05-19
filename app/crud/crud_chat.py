from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.chat import ChatUpdate, ChatCreate
from app.models.chat import Chat


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    def add_owner(self, db: Session, chat: Chat, owner: User) -> None:
        chat.owner = owner
        db.add(chat)
        db.commit()
        db.refresh(chat)


crud_chat = CRUDChat(Chat)
