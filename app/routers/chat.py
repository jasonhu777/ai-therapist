from fastapi import APIRouter, WebSocket

from services.chat_services import handle_chat

router = APIRouter(prefix="/chat", tags=["chat"])

@router.websocket("/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    await handle_chat(websocket)