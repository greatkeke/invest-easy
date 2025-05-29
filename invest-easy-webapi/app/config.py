from functools import lru_cache
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

class Settings(BaseSettings):
    allow_origins: str = os.getenv("allow_origins", "*")
    model_config = SettingsConfigDict(env_file=".env")

    @property
    def allow_origins_list(self) -> List[str]:
        list = [origin.strip() for origin in self.allow_origins.split(",")]
        for item in list:
            logging.warning(f"Allow origin: {item}")
        return list


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
