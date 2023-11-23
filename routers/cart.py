from datetime import datetime
from typing import Optional, Dict
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse

from cart_db import record_to_carts_db
from dependencies import get_cart, items_list, categories_list, templates

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    dependencies=[Depends(get_cart), Depends(items_list), Depends(categories_list), ],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def my_cart(request: Request, cart: Dict = Depends(get_cart)):
    response = templates.TemplateResponse(
        "cart.html",
        context={
            "request": request,
            "cart": cart,
        }
    )
    return response


@router.get("/get", response_class=JSONResponse)
async def form(request: Request, cart: Dict = Depends(get_cart)):
    return {'cart': cart} if cart else {'status': 200, 'cart': 'empty'}


@router.post("/add", response_class=JSONResponse)
async def add_to_cart(
        request: Request,
        name: Optional[str] = Form(...),
        quantity: Optional[str] = Form(...),
        color: Optional[str] = Form(...),
        data: Dict = Depends(items_list),
        cart: Dict = Depends(get_cart)
):

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
    request.session["cart"]["updated"] = datetime.now().strftime("%d %B %Y(%H:%M)")
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


@router.get("/update", response_class=JSONResponse)
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
    request.session["cart"]["updated"] = datetime.now().strftime("%d %B %Y(%H:%M)")
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


@router.get("/cart_update", response_class=HTMLResponse)
async def update_cart(
        request: Request,
        cart: Dict = Depends(get_cart)
):
    response = templates.TemplateResponse(
        "cart-widget-update.html",
        context={
            "request": request,
            "cart": cart,
        }
    )
    return response


@router.delete("/del", response_class=JSONResponse)
async def delete_cart(
        request: Request,
        cart: Dict = Depends(get_cart)):
    del request.session['cart']
    return {'status': 204, "cart": cart}


