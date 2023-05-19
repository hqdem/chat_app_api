import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Chat(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_ad = Column(DateTime, default=datetime.datetime.utcnow)
    owner = Column(Integer, ForeignKey('user.id'))

    users = relationship('User', secondary='chatuser')


class ChatUser(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), primary_key=True)
