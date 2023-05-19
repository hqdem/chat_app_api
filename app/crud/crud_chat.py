from app.crud.base import CRUDBase
from app.schemas.chat import ChatUpdate, ChatCreate, Chat


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    pass
