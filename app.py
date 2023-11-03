import json
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)

#
# @app.get("/a")
# async def session_set(request: Request):
#     request.session["my_var"] = "1234"
#     return 'ok'


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        context={"request": request}
    )


@app.get("/form", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse(
        "form.html",
        context={"request": request}
    )


@app.get("/cart", response_class=JSONResponse)
async def form(request: Request):
    cart = request.session.get('cart')
    if cart:
        result = {'cart': cart}
    else:
        result = {'status': 200, 'cart': cart}
    return result


@app.delete("/del", response_class=JSONResponse)
async def delete_cart(request: Request):
    del request.session['cart']
    return {'status': 204, "url_for": request.url}


@app.post("/item/{item_id}", response_class=HTMLResponse)
async def add(
        request: Request,
        name: str = Form(...),
        quantity: str = Form(...),

):
    with open("db.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("categoies.json", "r", encoding="utf-8") as с:
        categories = json.load(с)
    cart = request.session.get("cart", None)

    title = data.get('00' + str(name))['title']
    price = data.get('00' + str(name))['price']
    img = data.get('00' + str(name))['thumbnail']

    items = {
        name: {
            "name": title,
            "price": price,
            "quantity": int(quantity),
            "img": img,
        }
    }


    if cart:
        if name in cart.keys():
            request.session.get("cart")[name]['quantity'] += int(quantity)
        else:
            request.session.get("cart").update(items)
    else:
        request.session["cart"] = dict()
        request.session.get("cart").update(items)
    print('cart = ', cart)
    print('name = ', name)
    print('quantity = ', quantity)
    # if cart:
    #     check = ['true' for c in cart if c['name'] == items['name']]
    #     print('________________', check, len(check))
    #     if len(check) > 0:
    #         return {"request": request, "status": "error"}
    #     else:
    #         request.session["cart"].append(items)
    #
    # else:
    #     request.session["cart"] = []
    #     request.session.get("cart").append(items)
    context = {
        "request": request,
        "data": data.get('00'+str(name)),
        "categories": categories,
        "all_products": data,
        "cart": request.session.get("cart", None),
    }
    return templates.TemplateResponse(
        "item.html",
        context=context
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
    cart = request.session.get("cart")
    context = {
        "request": request,
        "data": data.get(item_id),
        "categories": categories,
        "all_products": data,
        "cart": cart,
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
