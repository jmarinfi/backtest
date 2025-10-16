from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_url_api_connect: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env", 
        env_file_encoding="utf-8"
    )


settings = Settings() # type: ignore
