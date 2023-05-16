from fastapi import APIRouter
from app.api.v1.endpoints import users, chats

api_router = APIRouter(prefix='')

api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(chats.router, prefix='/chats', tags=['chats'])
