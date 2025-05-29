import clients.ai_client as ai_client
import clients.aws_dynamodb as aws_dynamodb
from core.config import settings
from google.genai import types
from core import system_instructions


import uuid


def update_chat_context(role, content, chat_context):
    if content is not None and content.strip() != "":
        chat_context.append({"role": role, "content": content})
    
async def begin_session(user_id, user_email):
    try:
        chat_context = aws_dynamodb.load_session(user_id, user_email)    
        print('\nbegin_session start with chat_context:', chat_context)
        session_id = str(uuid.uuid4())

        gemini_chat_context = convert_chat_context_to_gemini(chat_context)
        # append_start_session_message_gemini(gemini_chat_context)
        assistant_message = ai_client.begin_session(gemini_chat_context)

        update_chat_context(settings.assistant_role, assistant_message, chat_context)
        aws_dynamodb.save_session(chat_context, user_id)        

        print('\nbegin_session end')

        return {"session_id": session_id, "assistant_message": assistant_message, "ended": False}

    except Exception as e:
        print(f"An error occurred in begin_session: {e}")
        
async def continue_session(session_id, user_message, user_id, user_email):
    try:
        chat_context = aws_dynamodb.load_session(user_id, user_email)        
        update_chat_context("user", user_message, chat_context)
        print('\ncontinue_session start')
        
        gemini_chat_context = convert_chat_context_to_gemini(chat_context)
        assistant_message = ai_client.continue_session(gemini_chat_context)
        print('\ncontinue_session assistant_message:', assistant_message)
        update_chat_context(settings.assistant_role, assistant_message, chat_context)
        aws_dynamodb.save_session(chat_context, user_id)        
        
        print('\ncontinue_session end')
        
        return {"session_id": session_id, "assistant_message": assistant_message, "ended": False}

    except Exception as e:
        print(f"An error occurred in continue_session: {e}")

async def end_session(session_id, user_id, user_email):
    try:
        print('\nend_session start')

        chat_context = aws_dynamodb.load_session(user_id, user_email)
        
        gemini_chat_context = convert_chat_context_to_gemini(chat_context)
        
        assistant_message = ai_client.end_session(gemini_chat_context)
        update_chat_context(settings.assistant_role, assistant_message, chat_context)
        aws_dynamodb.save_session(chat_context, user_id)        

        print('\nend_session end')
        return {"session_id": session_id, "assistant_message": assistant_message, "ended": True}
    except Exception as e:
        print(f"An error occurred in end_session: {e}")
        
def convert_chat_context_to_gemini(chat_context):
    chat_context_gemini = []
    
    for message in chat_context:
        if message['role'] == 'user':
            chat_context_gemini.append(
                types.UserContent(
                    parts=[types.Part.from_text(text=message['content'])],
                )
            )
        elif message['role'] == 'assistant':
            chat_context_gemini.append(types.ModelContent(
                parts=[types.Part.from_text(text=message['content'])],
            ))

    print('\nconvert_chat_context_to_gemini chat_context_gemini:', chat_context_gemini)
    
    if not chat_context_gemini:
        append_user_message_gemini(chat_context_gemini)
    elif chat_context_gemini[-1].role != 'user':
        append_user_message_gemini(chat_context_gemini)
    return chat_context_gemini

def convert_gemini_to_chat_context(chat_context_gemini):
    chat_context = []
    
    for message in chat_context_gemini:
        if message['role'] == 'user':
            chat_context.append({'role': 'user', 'content': message['parts'][0]['text']})
        elif message['role'] == 'model':
            chat_context.append({'role': 'assistant', 'content': message['parts'][0]['text']})

    return chat_context

def append_user_message_gemini(chat_context_gemini, user_message=""):
    print('\nappend_user_message')
    chat_context_gemini.append(types.UserContent(parts=[types.Part.from_text(text=user_message)]))
    return chat_context_gemini

# def append_start_session_message_gemini(chat_context_gemini):
#     print('\nappend_start_session_message')
#     append_user_message_gemini(chat_context_gemini, system_instructions.begin_session_instruction)
#     return chat_context_gemini