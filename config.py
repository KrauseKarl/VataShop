import os
import sys

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG")
PROJECT_ID = os.getenv("PROJECT_ID")
OST = sys.platform

WINDOWS = "win32"
LINUX = "linux"

# UVICORN ARGS
if OST == WINDOWS:
    APP = str(os.getenv("APP"))
    HOST = str(os.getenv("HOST_DEV", "127.0.0.1"))
    PORT = int(os.getenv("PORT_DEV"))
else:
    APP = str(os.getenv("APP"))
    HOST = str(os.getenv("HOST_DEV", "127.0.0.1"))
    PORT = int(os.getenv("PORT_DEV"))

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

# CART FOLDERS
if OST == WINDOWS:
    CART_DB_FOLDER = os.getenv("CART_DB_FOLDER_DEV")
    CART_ERROR_LOG = os.getenv("CART_ERROR_LOG_DEV")
else:
    CART_DB_FOLDER = os.getenv("CART_DB_FOLDER_PROD")
    CART_ERROR_LOG = os.getenv("CART_ERROR_LOG_PROD")
CART_DB_FILE = os.getenv("CART_DB_FILE")

# ORDER FOLDER
if OST == WINDOWS:
    ORDER_DB_PATH = os.getenv("ORDER_DB_PATH_DEV")
else:
    ORDER_DB_PATH = os.getenv("ORDER_DB_PATH_PROD")
ORDER_DB_FILE = os.getenv("ORDER_DB_FILE")

# ORIGINS
if OST == WINDOWS:
    ORIGINS = os.getenv("ORIGINS_DEV").split(" ")
else:
    ORIGINS = os.getenv("ORIGINS_PROD").split(" ")

# ALLOWED_HOST
if OST == WINDOWS:
    ALLOWED_HOST = os.getenv("ALLOWED_HOST_DEV").split(" ")
else:
    ALLOWED_HOST = os.getenv("ALLOWED_HOST_PROD").split(" ")


# POSTGRES
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")

# SECRET_AUTH = os.getenv("SECRET_AUTH")
