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
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


app.include_router(chat.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to AI Therapist"}

@app.get("/chat-ui")
async def chat_ui(request: Request):
    return HTMLResponse(html)

handler = Mangum(app)
# from fastapi import FastAPI, WebSocket
# from fastapi.responses import HTMLResponse
# from static.html_code import html_code
# from services.chat_service import handle_chat



# app = FastAPI(title="AI Therapist")


# @app.get("/")
# async def get():
#     return HTMLResponse(html_code)


# @app.websocket("/start_session")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     await handle_chat(websocket)
#     await websocket.close()

# @app.post("/create_account")
# async def create_account(data: dict):
#     try:
#         user_id = data.get("user_id")
#         chat_context = data.get("chat_context", [])
        
#         # Create a new user in DynamoDB
#         aws_cognito.create_account(data)
#         aws_dynamodb.create_account(user_id, chat_context)
        
#         return {"message": "Account created successfully", "user_id": user_id}
#     except Exception as e:
#         return {"error": str(e)}

# @app.post("/login")
# async def login(data: dict):
#     try:
#         user_id = data.get("user_id")
#         password = data.get("password")
        
#         # Authenticate user
#         if aws_cognito.authenticate_user(user_id, password):
#             return {"message": "Login successful", "user_id": user_id}
#         else:
#             return {"error": "Invalid credentials"}
#     except Exception as e:
#         return {"error": str(e)}

    
    
