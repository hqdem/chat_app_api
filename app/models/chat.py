import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Chat(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('user.id'))

    owner = relationship('User', foreign_keys='Chat.owner_id')
    users = relationship('User', secondary='chatuser', back_populates='chats')
    messages = relationship('Messages', back_populates='chat')


class ChatUser(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), primary_key=True)
