from core.chat_context import set_begin_session_system_instructions, set_end_session_system_instructions
from openai import OpenAI
from core import system_instructions
from core.config import settings

def get_ai_client():
    return OpenAI(api_key = settings.openai_api_key, base_url = settings.openai_base_url)
client = get_ai_client()

# This function sends a message to the AI client and returns the response.
def generate_response(chat_context, temperature=1.3):
    try:
        print(f"\n generate_response called with chat_context:", chat_context)

        response = client.chat.completions.create(
            model= settings.openai_model,
            messages=chat_context,
            stream=False,
            temperature=temperature,
            frequency_penalty=1,
        )
        print('\n\n generate_response received response:', response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def begin_session(chat_context):
    return generate_response(set_begin_session_system_instructions(chat_context), temperature=0.4)

def continue_session(chat_context):
    return generate_response(chat_context, temperature=1.3)

def end_session(chat_context):
    return generate_response(set_end_session_system_instructions(chat_context), temperature=0.4)