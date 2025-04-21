
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    openai_api_key: str = "sk-1933556094f645309c77f37495ddf825"
    openai_base_url: str = "https://api.deepseek.com"
    openai_model: str = "deepseek-chat"
    assistant_role: str = "assistant"
    user_role: str = "user"
    # aws_access_key_id: str
    # aws_secret_access_key: str
    # aws_region: str = "us-east-1"
    # cognito_user_pool_id: str
    # cognito_client_id: str
    dynamodb_table: str = "chat_sessions"

    class Config:
        env_file = ".env"

settings = Settings()