from google import genai
from google.genai import types
from core import system_instructions
from core.config import settings

def get_ai_client():
    return genai.Client(api_key=settings.gemini_api_key)
client = get_ai_client()

# This function sends a message to the AI client and returns the response.
def generate_response(chat_context, system_instruction, temperature=1.3):
    try:
        print(f"\n generate_response called with chat_context:", chat_context)

        print(f"\n generate_response called with system_instruction:", system_instruction)
        response = client.models.generate_content(
            model= settings.gemini_model,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature
            ),    
            contents=chat_context
        )
        print('\n\n generate_response received response:', response)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def begin_session(chat_context):
    return generate_response(chat_context, system_instruction=system_instructions.begin_session_system_instruction, temperature=0.4)

def continue_session(chat_context):
    return generate_response(chat_context, system_instruction=system_instructions.default_system_instruction, temperature=1.3)

def end_session(chat_context):
    return generate_response(chat_context, system_instruction=system_instructions.end_session_system_instruction, temperature=0.4)