import datetime
import json

import locale
import uuid

import uvicorn
from typing import Optional, Dict

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from starlette.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from cart_db import record_to_carts_db
from order_db import record_to_order_db
from task import send_order_email

locale.setlocale(
    category=locale.LC_ALL,
    locale="ru"
)

app = FastAPI()

# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     with open("db.json", "r", encoding="utf-8") as f:
#         data = json.load(f)


templates = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=31536000)


def items_list():
    with open("db.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def categories_list():
    with open("categoies.json", "r", encoding="utf-8") as с:
        categories = json.load(с)
    return categories


def get_cart(request: Request):
    cart = request.session.get('cart')
    if not cart:
        id_cart = str(uuid.uuid4())
        fake_cart = {
            "created": datetime.datetime.now().strftime("%d %B %Y(%H:%M)"),
            "updated": datetime.datetime.now().strftime("%d %B %Y(%H:%M)"),
            "id": id_cart,
            "item": {},
            "total": 0,
            "archived": False
        }
        request.session['cart'] = fake_cart
        record_to_carts_db(fake_cart)
    return cart


def get_category(items: Dict, category: str):
    return {k: v for k, v in items.items() if v['category'] == category}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {
        "request": request,
        "cart": get_cart(request),
        "categories": categories_list(),
        "products": items_list()
    }

    return templates.TemplateResponse(
        "index.html",
        context=context
    )


@app.get("/make-order", response_class=HTMLResponse)
async def make_order_form(request: Request):
    return templates.TemplateResponse(
        "order-form.html",
        context={
            "request": request,
            "cart": get_cart(request),
        }
    )


@app.get("/cart", response_class=JSONResponse)
async def form(request: Request):
    cart = get_cart(request)
    if cart:
        result = {'cart': cart}
    else:
        result = {'status': 200, 'cart': 'empty'}
    return result


@app.delete("/del-cart", response_class=JSONResponse)
async def delete_cart(request: Request):
    del request.session['cart']
    return {'status': 204, "cart": get_cart(request)}


@app.post("/add", response_class=JSONResponse)
async def add(
        request: Request,
        name: Optional[str] = Form(...),
        quantity: Optional[str] = Form(...),
        color: Optional[str] = Form(...),
):
    data = items_list()
    cart = get_cart(request)

    title = data.get('00' + str(name))['title']
    price = data.get('00' + str(name))['price']
    img = data.get('00' + str(name))["colors"][color]['img']
    color_name = data.get('00' + str(name))["colors"][color]['color_name']
    quantity = int(quantity)

    items = {
        color: {
            "name": title,
            "parent_id": '00' + str(name),
            "price": price,
            "quantity": quantity,
            "color": color,
            "color_name": color_name,
            "img": img,
            "summary": int(price) * int(quantity),
        }
    }
    total_sum = 0
    if cart:
        if color in list(request.session["cart"]["item"].keys()):
            request.session["cart"]["item"][color]['quantity'] += 1
            final_price = int(request.session["cart"]["item"][color]['price'])
            final_quantity = request.session["cart"]["item"][color]['quantity']
            final_summary = final_quantity * final_price
            request.session["cart"]["item"][color]['summary'] = final_summary
        else:
            request.session["cart"]["item"].update(items)
    else:
        request.session["cart"]["item"].update(items)
    record_to_carts_db(cart)
    for k, i in cart["item"].items():
        quant = int(i.get("quantity", 0))
        price = int(i.get("price"))
        total_sum += (quant * price)

    request.session["cart"]["total"] = total_sum
    request.session["cart"]["updated"] = datetime.datetime.now().strftime("%d %B %Y(%H:%M)")
    img_item = request.session['cart']['item'][color]['img']
    count_items = len(request.session["cart"].get("item").keys())
    return {
        "data": "OK",
        "item": len(cart["item"].keys()),
        "cart": cart,
        "product": data.get('00' + str(name)),
        "title": title,
        "count_items": count_items,
        "img": img_item

    }


@app.get("/cart-item-update", response_class=JSONResponse)
async def recalculate_cart(
        request: Request,
        item_id: Optional[str] = None,
        qty: Optional[int] = None
):
    extra_msg = None
    removed_id = None
    removed_all = None
    img_removed_item = None
    request.session["cart"]["total"] = 0
    if int(qty) < 1:
        extra_msg = "removed"
        removed_id = item_id
        img_removed_item = request.session['cart']['item'][item_id]['img']
        del request.session['cart']['item'][item_id]
    else:
        price = int(request.session["cart"]["item"][item_id]['price'])
        request.session['cart']['item'][item_id]['quantity'] = qty
        request.session["cart"]["item"][item_id]['summary'] = qty * price
        request.session["cart"]["total"] = 0
    if len(request.session["cart"]["item"]) > 0:
        for k, it in request.session["cart"]["item"].items():
            request.session["cart"]["total"] += int(it.get("summary"))
    else:
        removed_all = True
        request.session["cart"]["total"] = 0
    request.session["cart"]["updated"] = datetime.datetime.now().strftime("%d %B %Y(%H:%M)")
    record_to_carts_db(request.session["cart"])
    count_items = len(request.session["cart"].get("item").keys())
    context = {
        "status": "OK",
        "extra": extra_msg,
        "removed_id": removed_id,
        "removed_all": removed_all,
        "item_id": str(item_id),
        "cart": request.session["cart"],
        "count_items": count_items,
        "img": img_removed_item
    }

    return context


@app.get("/catalog", response_class=HTMLResponse)
async def catalog(
        request: Request,
        sort_by: Optional[str] = None
):
    products = items_list()
    if sort_by == 'price-asc':
        queryset = {k: v for k, v in sorted(products.items(), key=lambda x: int(x[1]["price"]))}
    elif sort_by == 'price-desc':
        queryset = {k: v for k, v in sorted(products.items(), key=lambda x: int(x[1]["price"]), reverse=True)}
    else:
        queryset = products

    context = {
        "cart": get_cart(request),
        "request": request,
        "categories": categories_list(),
        "all_products": queryset,
    }
    return templates.TemplateResponse(
        "catalog.html",
        context=context
    )


@app.get("/catalog-sort", response_class=HTMLResponse)
async def catalog(
        request: Request,
        sort_by: Optional[str] = None
):
    products = items_list()
    if sort_by == 'price-asc':
        queryset = {k: v for k, v in sorted(products.items(), key=lambda x: int(x[1]["price"]))}
    elif sort_by == 'price-desc':
        queryset = {k: v for k, v in sorted(products.items(), key=lambda x: int(x[1]["price"]), reverse=True)}
    else:
        queryset = products

    context = {
        "request": request,
        "status": "ok",
        "all_products": queryset,
    }
    return templates.TemplateResponse(
        "catalog.html",
        context=context
    )


@app.get("/category/{category}", response_class=HTMLResponse)
async def a_category_list(
        request: Request,
        sort_by: Optional[str] = None,
        category: Optional[str] = None
):
    products = items_list()

    if category in ['кашпо', 'свечи', 'вазы']:
        products = {k: v for k, v in products.items() if v['category'] == category}
    if sort_by == 'price-asc':
        products = {k: v for k, v in sorted(products.items(), key=lambda x: int(x[1]["price"]))}
    elif sort_by == 'price-desc':
        products = {k: v for k, v in sorted(products.items(), key=lambda x: int(x[1]["price"]), reverse=True)}

    context = {
        "cart": get_cart(request),
        "request": request,
        "categories": categories_list(),
        "all_products": products,
    }
    return templates.TemplateResponse(
        "catalog.html",
        context=context
    )


@app.get("/cart_update", response_class=HTMLResponse)
async def update_cart(request: Request):
    context = {
        "request": request,
        "cart": get_cart(request),
    }
    return templates.TemplateResponse(

        "cart_update.html",
        context=context
    )


@app.get("/my-cart", response_class=HTMLResponse)
async def my_cart(request: Request):
    context = {
        "request": request,
        "cart": get_cart(request),
    }
    return templates.TemplateResponse(
        "cart_view.html",
        context=context
    )


@app.get("/item/{item_id}", response_class=HTMLResponse)
async def item(item_id: str, request: Request):
    cart = get_cart(request)
    default = list(items_list().get(item_id)['colors'].keys())[0]
    context = {
        "request": request,
        "product": items_list().get(item_id),
        "categories": categories_list(),
        "all_products": items_list(),
        "cart": cart,
        "default": default
    }
    return templates.TemplateResponse(
        "item.html",
        context=context
    )


@app.post("/send-order", response_class=JSONResponse)
async def preorder(
        request: Request,
        name: Optional[str] = Form(...),
        email: Optional[str] = Form(...),
        phone: Optional[str] = Form(...),
        msg: Optional[str] = Form(...)):
    cart = request.session["cart"]
    data = {
        "date": datetime.datetime.now().strftime("%d %B %Y(%H:%M)"),
        "name": name,
        "email": email,
        "phone": phone,
        "msg": msg,
        "cart": cart
    }

    record_to_order_db(data)
    cart['archived'] = True
    record_to_carts_db(cart, msg="order")
    # send_order_email.apply_async(kwargs={'data': data})
    del request.session["cart"]
    # request.session["cart"]['total'] = {}
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None,
        "url": '/'
    }


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
