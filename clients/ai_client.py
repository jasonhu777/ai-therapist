from openai import OpenAI
from core.config import settings

def get_ai_client():
    return OpenAI(api_key = settings.openai_api_key, base_url = settings.openai_base_url)
client = get_ai_client()

# This function sends a message to the AI client and returns the response.
def generate_response(chat_context, temperature=1.3):
    try:
        response = client.chat.completions.create(
            model= settings.openai_model,
            messages=chat_context,
            stream=False,
            temperature=temperature,
            frequency_penalty=1,
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def begin_session(chat_context):
    print('begin_session called with chat_context:', chat_context)
    return generate_response(chat_context, temperature=0.4)

def continue_session(chat_context):
    return generate_response(chat_context)

def end_session(chat_context):
    return generate_response(chat_context, temperature=0.4)