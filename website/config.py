from dotenv import load_dotenv
import os


load_dotenv()

# Настройка Postgres
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")


# Ключ шифрования для JWT
SECRET_KEY = os.environ.get("SECRET_KEY")

# Настройка Redis
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

# Настройка TG бота
TOKEN = os.environ.get("TOKEN")
OWNER_ID = os.environ.get("OWNER_ID")
