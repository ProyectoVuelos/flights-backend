from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class to manage application configuration from environment variables.
    Pydantic automatically loads values from a `.env` file and validates them.

    Attributes:
        supabase_url (str): The URL for the Supabase project.
        supabase_key (str): The public (anon) API key for the Supabase project.
        uvicorn_host (str): The host for the Uvicorn server.
        uvicorn_port (int): The port for the Uvicorn server.
    """

    def __init__(self):
        super().__init__()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    supabase_url: str = Field(..., description="Supabase project URL is required")
    supabase_key: str = Field(..., description="Supabase project API key is required")
    uvicorn_host: str = Field("0.0.0.0", description="Uvicorn server host")
    uvicorn_port: int = Field(8000, description="Uvicorn server port")


settings = Settings()
