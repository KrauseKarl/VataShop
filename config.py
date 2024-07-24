import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")

# MAIL
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")

# TELEGRAM BOT
TOKEN_TG = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

# SESSION
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

# CELERY
CELERY_BROKER = os.getenv("CELERY_BROKER")
CELERY_BACKEND = os.getenv("CELERY_BACKEND")

# POSTGRES
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")

# SECRET_AUTH = os.getenv("SECRET_AUTH")