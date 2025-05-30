from core import system_instructions
from clients import aws_dynamodb
from static.initial_context import chat_context
from core.config import settings

def get_chat_context(user_id, user_email):
    try:
        return aws_dynamodb.load_session(user_id, user_email)
    except Exception as e:
        print(f"An error occurred while loading chat context: {e}")
    return chat_context

def update_chat_context(role, content, chat_context, user_id=None):
    if content is not None and content.strip() != "":
        chat_context.append({"role": role, "content": content})

def save_chat_context(chat_context, user_id, user_email):
    try:
        aws_dynamodb.save_session(chat_context, user_id, user_email)
    except Exception as e:
        print(f"An error occurred while saving chat context: {e}")

def set_begin_session_system_instructions(chat_context):
    update_chat_context(settings.system_role, system_instructions.begin_session_rules, chat_context)
    return chat_context

def set_end_session_system_instructions(chat_context):
    update_chat_context(settings.system_role, system_instructions.end_session_rules, chat_context)
    return chat_context


