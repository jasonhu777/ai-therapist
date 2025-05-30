from core.chat_context import get_chat_context, save_chat_context, update_chat_context
import clients.ai_client as ai_client
import clients.aws_dynamodb as aws_dynamodb
from core.config import settings



import uuid


    
async def begin_session(user_id, user_email):
    try:
        chat_context = get_chat_context(user_id, user_email)    
        print('\nbegin_session start with chat_context:', chat_context)
        session_id = str(uuid.uuid4())

        assistant_message = ai_client.begin_session(chat_context)
        update_chat_context(settings.assistant_role, assistant_message, chat_context, user_id)
        save_chat_context(chat_context, user_id, user_email)
        
        print('\nbegin_session end')
        return {"session_id": session_id, "assistant_message": assistant_message, "ended": False}

    except Exception as e:
        print(f"An error occurred in begin_session: {e}")
        
async def continue_session(session_id, user_message, user_id, user_email):
    try:
        chat_context = get_chat_context(user_id, user_email)
        update_chat_context(settings.user_role, user_message, chat_context, user_id)
        print('\ncontinue_session start')
        

        assistant_message = ai_client.continue_session(chat_context)
        print('\ncontinue_session assistant_message:', assistant_message)
        update_chat_context(settings.assistant_role, assistant_message, chat_context, user_id)
        save_chat_context(chat_context, user_id, user_email)
        
        print('\ncontinue_session end')
        return {"session_id": session_id, "assistant_message": assistant_message, "ended": False}

    except Exception as e:
        print(f"An error occurred in continue_session: {e}")

async def end_session(session_id, user_id, user_email):
    try:
        print('\nend_session start')
        chat_context = get_chat_context(user_id, user_email)

        assistant_message = ai_client.end_session(chat_context=chat_context)
        update_chat_context(settings.assistant_role, assistant_message, chat_context, user_id)
        save_chat_context(chat_context, user_id, user_email)
        
        print('\nend_session end')
        return {"session_id": session_id, "assistant_message": assistant_message, "ended": True}
    except Exception as e:
        print(f"An error occurred in end_session: {e}")
        

