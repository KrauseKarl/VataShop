import json
import locale
import logging
import sys

import uvicorn
from typing import Dict

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi_sessions import session_verifier
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from config import APP, HOST, PORT, DEBUG
from config import OST, WINDOWS
from config import ORIGINS
from config import ALLOWED_HOST
from config import SESSION_SECRET_KEY
from routers import catalog
from routers import cart
from routers import favorite
from routers import order
from dependencies import get_cart
from dependencies import categories_list
from dependencies import items_list
from dependencies import templates

if OST == WINDOWS:
    locale.setlocale(
        category=locale.LC_ALL,
        locale="ru_RU.UTF-8"
    )

logging.basicConfig(
    stream=sys.stdout,
    level="INFO",
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S",
)
logger = logging.getLogger("vataShop")

app = FastAPI()
app.include_router(catalog.router)
app.include_router(cart.router)
app.include_router(favorite.router)
app.include_router(order.router)

# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     with open("db.json", "r", encoding="utf-8") as f:
#         data = json.load(f)

app.mount(
    "/assets",
    StaticFiles(directory="assets"),
    name="assets"
)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    max_age=14 * 24 * 60 * 60
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=ALLOWED_HOST
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_origins=ORIGINS,
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {
        "request": request,
        "cart": get_cart(request),
        "categories": categories_list(),
        "products": [i for i in items_list().values()]
    }

    return templates.TemplateResponse(
        "index.html",
        context=context
    )


if __name__ == '__main__':
    try:
        uvicorn.run(app=APP, host=HOST, port=PORT, reload=True)
    except Exception as error:
        logger.error(error)
