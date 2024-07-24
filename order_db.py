import json

from typing import Dict

ORDER_DB_PATH = './orders/order_db.json'


def create_order_json():
    with open(ORDER_DB_PATH, 'w', encoding='utf-8') as f:
        order_dict = {
            "orders": {}
        }
        json.dump(order_dict, f, indent=4, ensure_ascii=False)


def update_order_json(order: Dict):
    with open(ORDER_DB_PATH, "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        try:
            current_key = int(list(data["orders"].keys())[-1]) + 1
        except (KeyError, IndexError):
            current_key = '1'
    order["order_id"] = current_key
    data["orders"][current_key] = order

    with open(ORDER_DB_PATH, "w", encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile, indent=4, ensure_ascii=False)
    return current_key


async def record_to_order_db(order: Dict):
    try:
        current_key = update_order_json(order)
    except Exception:
        create_order_json()
        current_key = update_order_json(order)
    return current_key
