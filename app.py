import json
from typing import Optional, Dict

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from services import add_cart

app = FastAPI()
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
    fake_cart = {
        "item": {},
        "total": 0
    }
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = fake_cart
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
):
    data = items_list()
    cart = get_cart(request)

    title = data.get('00' + str(name))['title']
    price = data.get('00' + str(name))['price']
    img = data.get('00' + str(name))['thumbnail']
    quantity = int(quantity)

    items = {
        name: {
            "name": title,
            "price": price,
            "quantity": quantity,
            "img": img,
            "summary": int(price) * int(quantity),
        }
    }
    total_sum = 0
    if cart:
        if name in cart.keys():
            price = int(request.session["cart"]["item"][name]['price'])
            in_cart_qnt = int(request.session["cart"]["item"][name]['quantity'])
            if quantity == 0:
                del request.session["cart"]["item"][name]
            elif in_cart_qnt > quantity:
                request.session["cart"]["item"][name]['quantity'] = quantity
            else:
                request.session["cart"]["item"][name]['quantity'] = quantity
            for k, i in items.items():
                total_sum += int(i.get("quantity", 0))
            request.session["cart"]["item"][name]['summary'] = quantity * price
        else:
            request.session["cart"]["item"].update(items)
    else:
        request.session["cart"]["item"].update(items)

    for k, i in cart["item"].items():
        quant = int(i.get("quantity", 0))
        price = int(i.get("price"))
        total_sum += (quant * price)

    request.session["cart"]["total"] = total_sum
    img_item = request.session['cart']['item'][name]['img']
    # return templates.TemplateResponse("item.html", context=context)
    count_items = len(request.session["cart"].get("item").keys())
    context = {
        "data": "OK",
        "item": len(cart["item"].keys()),
        "cart": cart,
        "product": data.get('00' + str(name)),
        "count_items": count_items,
        "img": img_item

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
        sort_by: Optional[str]=None,
        category: Optional[str]=None
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
        "cart": request.session["cart"],
    }
    return templates.TemplateResponse(
        "cart_view.html",
        context=context
    )


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
    count_items = len(request.session["cart"].get("item").keys())
    return {
        "status": "OK",
        "extra": extra_msg,
        "removed_id": removed_id,
        "removed_all": removed_all,
        "item_id": str(item_id),
        "cart": request.session["cart"],
        "count_items": count_items,
        "img": img_removed_item
    }


@app.get("/item/{item_id}", response_class=HTMLResponse)
async def item(item_id: str, request: Request):
    cart = get_cart(request)
    context = {
        "request": request,
        "product": items_list().get(item_id),
        "categories": categories_list(),
        "all_products": items_list(),
        "cart": cart,
    }
    return templates.TemplateResponse(
        "item.html",
        context=context
    )


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
