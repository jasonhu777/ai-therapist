import ai_client
import aws_dynamodb

async def chat(websocket):
    chat_context = aws_dynamodb.get_chat_context()
    print(f"Chat context: {chat_context}")
    await begin_session(websocket, chat_context)
    
    while True:
        user_message = await get_user_message(websocket, chat_context)
        if "end session" in user_message: 
            break
        await continue_session(websocket, chat_context, user_message)
    
    await end_session(websocket, chat_context)
    
async def output_assistant_message(websocket, message):
    try:
        await websocket.send_text(f"Message from assistant: {message}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
async def output_user_message(websocket, message):
    try:
        await websocket.send_text(f"Message from user: {message}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
async def get_user_message(websocket, chat_context):
    try:
        print("Waiting for user message...")
        user_message = await websocket.receive_text()
        update_chat_context("user", user_message, chat_context)
        print(f"Received user message: {user_message}")
        return user_message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def update_chat_context(role, content, chat_context):
    chat_context.append({"role": role, "content": content})
    

async def begin_session(websocket, chat_context):
    try:
        print('begin_session start')
        update_chat_context("system", "If you did not find any history, treat the user as a NEW CLIENT. Grant the user a warm welcome, and ask about the problems that you have discussed in the previous session. Ask the user if they want to continue the session or start a new one.", chat_context)
        assistant_message = ai_client.begin_session(chat_context).choices[0].message.content
        await output_assistant_message(websocket, assistant_message)
        update_chat_context("assistant", assistant_message, chat_context)
        print('begin_session end')

    except Exception as e:
        print(f"An error occurred: {e}")
        
async def continue_session(websocket, chat_context, user_message):
    try:
        await output_user_message(websocket, user_message)
        
        print('continue_session start')
        
        await output_user_message(websocket, user_message)
        
        assistant_message = ai_client.continue_session(chat_context).choices[0].message.content
        await output_assistant_message(websocket, assistant_message)
        update_chat_context("assistant", assistant_message, chat_context)
        
        print(chat_context)
        print('continue_session end')
        
    except Exception as e:
        print(f"An error occurred: {e}")

async def end_session(websocket, chat_context):
    try:
        print('end_session start')
        
        update_chat_context("system", "The session has ended. Generate a summary of the conversation, output the summary into bullet points. Outlines the emotions of the user, on a scale of 1 to 10, how strong these emotions are, and how the user felt during the session. The summary should be concise and easy to read. If there is not enough information, just output talk to you next time.", chat_context)
        assistant_message = ai_client.end_session(chat_context).choices[0].message.content
        await output_assistant_message(websocket, assistant_message)
        update_chat_context("assistant", assistant_message, chat_context)
        aws_dynamodb.update_chat_context(chat_context)        
        await websocket.close()
        print('end_session end')
    except Exception as e:
        print(f"An error occurred: {e}")