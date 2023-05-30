from pydantic import BaseModel

from app.schemas.chat import Chat
from app.schemas.user import User


class MessageBase(BaseModel):
    data: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class MessageInDBBase(MessageBase):
    id: int
    chat: Chat
    sender: User

    class Config:
        orm_mode = True


class Message(MessageInDBBase):
    pass
