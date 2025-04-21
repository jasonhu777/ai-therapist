from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from core.logging import logger
from routers import chat

app = FastAPI(title="AI Therapist")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

templates = Jinja2Templates(directory="static")

app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Therapist"}

@app.get("/chat-ui")
def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})