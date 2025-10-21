# File: app/core/config.py
import os
from dotenv import load_dotenv

env_file = ".env.dev" if os.getenv("ENV") == "development" else ".env"

# Carga las variables de entorno desde el archivo correspondiente
load_dotenv(dotenv_path=env_file)

class Settings:
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")

    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

settings = Settings()