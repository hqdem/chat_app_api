from pydantic import BaseModel

from app.schemas.chat import Chat
from app.schemas.user import User


class MessageBase(BaseModel):
    data: str


class MessageCreate(MessageBase):
    chat_id: int
    sender_id: int


class MessageInDBBase(MessageBase):
    id: int
    chat: Chat
    sender: User


class Message(MessageInDBBase):
    pass
