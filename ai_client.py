from openai import OpenAI

def get_ai_client():
    return OpenAI(api_key="sk-1933556094f645309c77f37495ddf825", base_url="https://api.deepseek.com")
client = get_ai_client()

# This function sends a message to the AI client and returns the response.
def send_message_to_ai_client(chat_context, temperature=1.3, model="deepseek-chat"):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=chat_context,
            stream=False,
            temperature=1.3,
            frequency_penalty=1,
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def begin_session(chat_context):
    return send_message_to_ai_client(chat_context, temperature=0.4)

def continue_session(chat_context):
    return send_message_to_ai_client(chat_context)

def end_session(chat_context):
    return send_message_to_ai_client(chat_context, temperature=0.4)