# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Autismo Mochis IA"

    # 🔐 Seguridad / JWT
    SECRET_KEY: str

    # 🗄 Base de datos
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost/AutismoMochis"

    # 📩 SMTP / Correos
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    SMTP_FROM_NAME: str = "Autismo Mochis IA"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
