import json

from typing import Dict

ORDER_DB_PATH = './carts/carts_db.json'


def create_carts_json():
    with open(ORDER_DB_PATH, 'w', encoding='utf-8') as f:
        order_dict = {
            "carts": {}
        }
        json.dump(order_dict, f, indent=4, ensure_ascii=False)


def update_carts_json(order: Dict):
    with open(ORDER_DB_PATH, "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        try:
            current_key = int(list(data["carts"].keys())[-1]) + 1
        except (KeyError, IndexError):
            current_key = '1'
    data["carts"][current_key] = order
    with open(ORDER_DB_PATH, "w", encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile, indent=4, ensure_ascii=False)


def record_to_carts_db(cart: Dict):
    try:
        update_carts_json(cart)
    except Exception:
        create_carts_json()
        update_carts_json(cart)
