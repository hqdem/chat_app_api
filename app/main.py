from fastapi import FastAPI

from app.api.v1.api_router import api_router
from app.core.config import settings

app = FastAPI()
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get('/')
def root():
    return 'All working now'
