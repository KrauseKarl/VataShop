import json
import uuid
from typing import Dict
from datetime import datetime
from fastapi import Request, Query
from starlette.templating import Jinja2Templates

from cart_db import record_to_carts_db

templates = Jinja2Templates(directory="templates")


def today():
    return datetime.now().strftime("%d %B %Y(%H:%M)")


def items_list():
    with open("db/products.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def categories_list():
    with open("db/categories.json", "r", encoding="utf-8") as с:
        categories = json.load(с)
    return categories


def get_cart(request: Request):
    cart = request.session.get('cart')
    if not cart:
        id_cart = str(uuid.uuid4())
        fake_cart = {
            "created": datetime.now().strftime("%d %B %Y(%H:%M)"),
            "updated": datetime.now().strftime("%d %B %Y(%H:%M)"),
            "id": id_cart,
            "item": {},
            "total": 0,
            "archived": False
        }
        request.session['cart'] = fake_cart
        record_to_carts_db(fake_cart)
    return cart


def get_favorite(request: Request):
    favorites = request.session.get('favorite')
    if not favorites:
        request.session['favorite'] = {}
    return request.session['favorite']


def get_category(items: Dict, category: str):
    return {
        k: v for k, v in items.items()
        if v['category'] == category
    }


def get_pagination_params(
        offset: int = Query(0, ge=0),
        limit: int = Query(3, gt=0)
):
    return {"offset": offset, "limit": limit}
