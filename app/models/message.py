from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String)
    sender_id = Column(Integer, ForeignKey('user.id'))
    chat_id = Column(Integer, ForeignKey('chat.id'))

    chat = relationship('Chat', back_populates='messages')
    sender = relationship('User', back_populates='messages')
