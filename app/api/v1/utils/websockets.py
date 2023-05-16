from typing import List

from fastapi import WebSocket, WebSocketException, status
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.crud_user import crud_user
from app.schemas.token import WebSocketTokenPayload, TokenPayload
from app.models.user import User


class ConnectionManager:
    def __init__(self):
        self._active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self._active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket, code=status.WS_1000_NORMAL_CLOSURE, reason=''):
        self._active_connections.remove(websocket)
        await websocket.close(code=code, reason=reason)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_message(self, message: str):
        for websocket in self._active_connections:
            await websocket.send_text(message)

    async def authenticate_user(self, db: Session, creds: WebSocketTokenPayload, websocket: WebSocket) -> User:
        try:
            payload = jwt.decode(creds, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            token_data = TokenPayload(**payload)
        except (jwt.JWTError, ValidationError):
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Couldn't validate credentials")
        user = crud_user.get_user_by_login(db, login=token_data.sub)
        if not user:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason='User not found')
        return user
