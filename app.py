import json
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        context={"request": request}
    )


@app.get("/more", response_class=HTMLResponse)
async def more(request: Request):
    return templates.TemplateResponse(
        "more.html",
        context={"request": request}
    )


@app.get("/catalog", response_class=HTMLResponse)
async def catalog(request: Request):
    with open("db.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("categoies.json", "r", encoding="utf-8") as с:
        categories = json.load(с)
    context = {
        "request": request,
        "categories": categories,
        "all_products": data,
    }
    return templates.TemplateResponse(
        "catalog.html",
        context=context
    )


@app.get("/item/{item_id}", response_class=HTMLResponse)
async def item(item_id, request: Request):

    with open("db.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("categoies.json", "r", encoding="utf-8") as с:
        categories = json.load(с)
    print(item_id)
    context = {
        "request": request,
        "data": data.get(item_id),
        "categories": categories,
        "all_products": data,
    }
    return templates.TemplateResponse(
        "item.html",
        context=context
    )
@app.get("/items/{item_id}", response_class=HTMLResponse)
async def item2(item_id, request: Request):

    with open("db.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"status": 200, "data": data.get(item_id)}


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
