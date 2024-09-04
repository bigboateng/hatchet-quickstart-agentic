from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    hatchet_client_token: str
    debug: bool = True
    slack_bot_token: str
    openai_api_key: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()

