from datetime import datetime
from typing import Optional, Dict
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse

from cart_db import record_to_carts_db
from config import DATE_FORMAT
from dependencies import get_cart
from dependencies import items_list
from dependencies import categories_list
from dependencies import templates
from logger import logger

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    dependencies=[
        Depends(get_cart),
        Depends(items_list),
        Depends(categories_list),
    ],
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
    # try:
        total_sum = 0
        parent_id = '00' + str(name)
        color_id = color
        title = data.get(parent_id).get('title')
        img = data.get(parent_id).get("colors").get(color).get('img')
        color_name = data.get(parent_id).get("colors").get(color).get('color_name')
        new_items = {
            color_id: {
                "name": title,
                "parent_id": parent_id,
                "price": int(data.get(parent_id).get('price')),
                "quantity": int(quantity),
                "color": color_id,
                "color_name": color_name,
                "color_code": data.get(parent_id).get("colors").get(color).get('color_code'),
                "img": img,
                "summary": int(data.get(parent_id).get('price')) * int(quantity),
            }
        }

        if cart:
            if str(color) in list(request.session["cart"]["item"].keys()):
                print("yes")
                print('4*', request.session["cart"]["item"][color_id]['quantity'])
                quantity = int(request.session["cart"]["item"][color_id]['quantity']) + 1
                request.session["cart"]["item"][color_id]['quantity'] = str(quantity)
                print('5*', request.session["cart"]["item"][color_id]['quantity'])

                final_price = int(request.session["cart"]["item"][color_id]['price'])
                final_quantity = int(request.session["cart"]["item"][color_id]['quantity'])
                final_summary = final_quantity * final_price
                request.session["cart"]["item"][color_id]['summary'] = final_summary
            else:
                request.session["cart"]["item"].update(new_items)
        else:
            print("add new item")
            request.session["cart"]["item"] = new_items
        record_to_carts_db(cart)

        for key, item in cart["item"].items():
            quant = int(item.get("quantity", 0))
            price = int(item.get("price"))
            total_sum += (quant * price)
        now = datetime.now().strftime("%d %B %Y(%H:%M)")
        request.session["cart"]["total"] = total_sum
        request.session["cart"]["updated"] = now

        response = {
            "data": "OK",
            "count_items": len(cart["item"].keys()),
            "title": title,
            "color_name": color_name,
            "img": img,
            "total": total_sum,
            "cart": request.session["cart"],
            "product": data.get(parent_id),
        }
    # except Exception as error:
    #     logger.error(error)
    #     response = {"data": error}
        return response


@router.get("/update", response_class=JSONResponse)
async def recalculate_cart(
        request: Request,
        item_id: Optional[str] = None,
        qty: Optional[int] = None
):
    extra_msg = None
    removed_id = None
    removed_all = None
    img_removed_item = request.session['cart']['item'][item_id]['img']
    request.session["cart"]["total"] = 0
    quantity = int(qty)
    if quantity < 1:
        extra_msg = "removed"
        removed_id = item_id
        del request.session['cart']['item'][item_id]
    else:
        price = int(request.session["cart"]["item"][item_id]['price'])
        request.session['cart']['item'][item_id]['quantity'] = quantity
        request.session["cart"]["item"][item_id]['summary'] =  quantity * price
        request.session["cart"]["total"] = 0
    if len(request.session["cart"]["item"]) > 0:
        for k, it in request.session["cart"]["item"].items():
            request.session["cart"]["total"] += int(it.get("summary"))
    else:
        removed_all = True
        request.session["cart"]["total"] = 0
    request.session["cart"]["updated"] = datetime.now().strftime(DATE_FORMAT)
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
        "img": img_removed_item,
        "total": request.session["cart"]["total"]
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
