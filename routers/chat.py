from fastapi import APIRouter, WebSocket

from services.chat_service import handle_chat

router = APIRouter(prefix="/chat", tags=["chat"])

@router.websocket("/start_session")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    await handle_chat(websocket)
    await websocket.close()