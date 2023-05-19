from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import User


class ChatBase(BaseModel):
    name: str


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    pass


class ChatInDBBase(ChatBase):
    id: int
    name: str
    created_at: datetime
    owner: User


class Chat(ChatInDBBase):
    pass
