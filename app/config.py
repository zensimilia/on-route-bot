from typing import Optional
from pydantic import BaseSettings


class AppConfig(BaseSettings):
    """Global application configurations.

    Variables will be loaded from the .env file. However, if
    there is a shell environment variable having the same name,
    that will take precedence.
    """

    DEBUG: bool = False
    BOT_TOKEN: str
    DB_FILE: str = 'data.sqlite'
    LOG_CONFIG: Optional[dict] = None

    class Config:
        """Load variables from the dotenv file."""

        env_file: str = '.env'
        env_file_encoding: str = 'utf-8'


Config = AppConfig()
