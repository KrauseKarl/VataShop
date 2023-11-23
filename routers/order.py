from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse

from cart_db import record_to_carts_db
from dependencies import get_cart, items_list, categories_list, templates, get_favorite, today
from order_db import record_to_order_db

router = APIRouter(
    prefix="/order",
    tags=["order"],
    dependencies=[Depends(get_cart), Depends(items_list), Depends(categories_list), ],
    responses={404: {"description": "Not found"}},
)
@router.get("/form", response_class=HTMLResponse)
async def order_form(request: Request):
    return templates.TemplateResponse(
        "order-form.html",
        context={
            "request": request,
            "cart": get_cart(request),
        }
    )


@router.post("/send", response_class=JSONResponse)
async def preorder(
        request: Request,
        now: datetime = Depends(today),
        cart: Dict = Depends(get_cart),
        favorites: Dict = Depends(get_favorite),
        name: Optional[str] = Form(...),
        email: Optional[str] = Form(...),
        phone: Optional[str] = Form(...),
        msg: Optional[str] = None):
    data = {
        "date": now,
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

    for prod in request.session["cart"]['item'].values():
        yesterday = datetime.today() - timedelta(days=1)
        prod["date"] = yesterday.strftime("%d %B %Y")
    favorites.update(request.session["cart"]['item'])

    del request.session["cart"]
    # request.session["cart"]['total'] = {}
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None,
        "url": '/'
    }
