from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.v1.utils.websockets import ConnectionManager

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:8000/api/v1/chats/ws_chat");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.websocket('/ws_chat')
async def start_chat(db: Annotated[Session, Depends(get_db)],
                     manager: Annotated[ConnectionManager, Depends(ConnectionManager)], websocket: WebSocket):
    await manager.connect(websocket)
    creds_data = await websocket.receive_text()

    try:
        await manager.authenticate_user(db, creds_data, websocket)
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Message text was: {data}", websocket)
    except WebSocketException as ex:
        await manager.disconnect(websocket, code=ex.code, reason=ex.reason)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_html():
    return HTMLResponse(html)
