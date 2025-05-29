from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from core.logging import logger
from routers import chat
from mangum import Mangum
from static.test_html import html

app = FastAPI(title="AI Therapist")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to AI Therapist"}

handler = Mangum(app)


    
    
