from sqlalchemy import Column, Integer, String, Boolean

from app.db.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    nickname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
