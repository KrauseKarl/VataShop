import datetime
import json
import os

from typing import Dict

CART_DB_FOLDER = './carts'
CART_DB_FILE = 'carts_db.json'
CART_DB_PATH = os.path.join(CART_DB_FOLDER, CART_DB_FILE)


def create_carts_json():
    if not os.path.exists(CART_DB_FOLDER):
        os.makedirs(CART_DB_FOLDER)
    with open(CART_DB_PATH, 'w', encoding='utf-8') as f:
        carts_dict = {
            "carts": {}
        }
        json.dump(carts_dict, f, indent=4, ensure_ascii=False)


def update_carts_json(cart: Dict, **kwargs):
    with open(CART_DB_PATH, "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    current_cart = cart["id"]
    if cart["id"] in data["carts"].keys():
        if not data["carts"][current_cart]["archived"]:
            if len(cart['item'].keys()) < 1 or kwargs['msg'] == "order":
                data["carts"][current_cart]["archived"] = True
            else:
                data["carts"][current_cart]["item"] = cart['item']
                data["carts"][current_cart]["total"] = cart['total']
                data["carts"][current_cart]["updated"] = datetime.datetime.now().strftime("%d %B %Y(%H:%M)")
    else:
        data["carts"][current_cart] = cart
    with open(CART_DB_PATH, "w", encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile, indent=4, ensure_ascii=False)


def record_to_carts_db(cart: Dict, **kwargs):
    try:
        update_carts_json(cart)
    except Exception:
        create_carts_json()
        update_carts_json(cart, **kwargs)
