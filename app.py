import locale
from typing import Dict

import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from dependencies import get_cart, categories_list, items_list
from routers import catalog, cart, favorite, order
from dependencies import templates

locale.setlocale(category=locale.LC_ALL, locale="ru")

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

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=31536000)


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
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
