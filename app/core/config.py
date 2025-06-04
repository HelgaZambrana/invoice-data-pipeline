from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    ENABLE_DEV_ENDPOINTS: bool = False  # Por defecto desactivado

    class Config:
        env_file = ".env"  # Especifica que lea desde el archivo .env

settings = Settings()