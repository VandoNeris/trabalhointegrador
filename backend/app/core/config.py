from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Configurações do Banco de Dados
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    
    # Configurações de Autenticação
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = Path(__file__).resolve().parents[3] / ".env"

settings = Settings()
