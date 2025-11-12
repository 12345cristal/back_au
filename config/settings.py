from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Autismo Mochis IA"
    SECRET_KEY: str = "baed92fd55877b5e82cf17fce0f3fae5d35ed266f7262afdc046bbc3048bf231"  # cámbialo por uno propio
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost/AutismoMochis"

settings = Settings()
