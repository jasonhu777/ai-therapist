from fastapi import APIRouter
from pydantic import BaseModel

from services import chat_service

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

class StartRequest(BaseModel):
    user_id: str
    user_email: str
    
class StartResponse(BaseModel):
    session_id: str
    assistant_message: str
    ended: bool = False

class MessageRequest(BaseModel):
    session_id: str
    message: str
    user_id: str
    user_email: str
        

class MessageResponse(BaseModel):
    session_id: str
    assistant_message: str
    ended: bool = False
    
class EndRequest(BaseModel):
    session_id: str
    user_id: str
    user_email: str

class EndResponse(BaseModel):
    session_id: str
    assistant_message: str
    ended: bool = False
    
@router.post("/start_session", response_model=StartResponse)
async def start_session(request: StartRequest):
    return await chat_service.begin_session(request.user_id, request.user_email)

@router.post("/message", response_model=MessageResponse)
async def message(request: MessageRequest):
    return await chat_service.continue_session(request.session_id, request.message, request.user_id, request.user_email)


@router.post("/end_session", response_model=EndResponse)
async def end_session(request: EndRequest):
    return await chat_service.end_session(request.session_id, request.user_id, request.user_email)
