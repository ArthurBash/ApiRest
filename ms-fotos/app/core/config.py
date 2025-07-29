from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
