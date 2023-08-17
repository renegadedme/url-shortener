#url_shortener/config.py
# defines the configuration of the app

from functools import lru_cache         #using LRU strategy for caching
from pydantic import BaseSettings       #pydantic validates data and manages settings

class Settings(BaseSettings):           #defines a subclass of BaseSettings
    env_name: str = 'Local'
    base_url: str = 'http://localhost:8000'
    db_url: str = 'sqlite:///./shortener.db'

    class Config:                       #this class lets pydantic load your environment variables from the .env file
        env_file = '.env'

@lru_cache                              #lru_cache decorator caches the output of the function so the get_settings()
def get_settings() -> Settings:
    settings = Settings()
    print(f'Loading settings for: {settings.env_name}')
    return settings
