import ai_client
import aws_cognito
from aws_dynamodb import create_table
import aws_dynamodb
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from html_code import html_code
from chat import chat
import uvicorn

from datetime import datetime



app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse(html_code)


@app.websocket("/start_session")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await chat(websocket)

@app.post("/create_account")
async def create_account(data: dict):
    try:
        user_id = data.get("user_id")
        chat_context = data.get("chat_context", [])
        
        # Create a new user in DynamoDB
        aws_cognito.create_account(data)
        aws_dynamodb.create_account(user_id, chat_context)
        
        return {"message": "Account created successfully", "user_id": user_id}
    except Exception as e:
        return {"error": str(e)}

@app.post("/login")
async def login(data: dict):
    try:
        user_id = data.get("user_id")
        password = data.get("password")
        
        # Authenticate user
        if aws_cognito.authenticate_user(user_id, password):
            return {"message": "Login successful", "user_id": user_id}
        else:
            return {"error": "Invalid credentials"}
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
