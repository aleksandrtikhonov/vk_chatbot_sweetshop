from pydantic import BaseSettings

from vk_bot.const import VK_API_VERSION


class Settings(BaseSettings):
    VK_API_TOKEN: str
    VK_CLUB_ID: str
    VK_API_VERSION: str = VK_API_VERSION

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
