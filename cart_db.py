import os
import json
import datetime

from typing import Dict

from config import CART_DB_FOLDER
from config import CART_DB_FILE
from config import CART_ERROR_LOG


CART_DB_PATH = os.path.join(CART_DB_FOLDER, CART_DB_FILE)
MODE_A = "a"
MODE_R = "r"
MODE_W = "w"


def create_carts_json():
    if not os.path.exists(CART_DB_FOLDER):
        os.makedirs(CART_DB_FOLDER)
        with open(CART_DB_PATH, mode=MODE_A, encoding='utf-8') as f:
            carts_dict = {}
            json.dump(carts_dict, f, indent=4, ensure_ascii=False)


def update_carts_json(cart: Dict, **kwargs):
    create_carts_json()
    with open(CART_DB_PATH, mode=MODE_R, encoding='utf-8') as jsonFile:
        all_carts = json.load(jsonFile)
        cart_id = cart["id"]
    new_cart = {cart_id: cart}
    if cart_id in list(all_carts.keys()):
        all_carts[cart_id] = cart
    else:
        all_carts.update(new_cart)
    with open(CART_DB_PATH, mode=MODE_W, encoding='utf-8') as jsonFile:
        json.dump(all_carts, jsonFile, indent=4, ensure_ascii=False)


def record_to_carts_db(cart: Dict, **kwargs):
    try:
        update_carts_json(cart)
    except Exception as e:
        with open(CART_ERROR_LOG, mode=MODE_A, encoding='utf-8') as f:
            date = datetime.datetime.now().strftime("%B-%d-%Y (%H:%M)")
            error = str(e)
            message = f"{date} {error}\n"
            f.write(message)
