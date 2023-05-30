from app.crud.base import CRUDBase
from app.models.message import Message
from app.schemas.messages import MessageCreate, MessageUpdate


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    pass


crud_message = CRUDMessage(Message)
