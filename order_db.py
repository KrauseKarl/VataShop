import os
import json
from typing import Dict

from config import ORDER_DB_PATH
from config import ORDER_DB_FILE

ORDER_DB_FILE = os.path.join(ORDER_DB_PATH, ORDER_DB_FILE)


def create_order_json():
    with open(ORDER_DB_FILE, 'w', encoding='utf-8') as f:
        order_dict = {"orders": {}}
        json.dump(order_dict, f, indent=4, ensure_ascii=False)


def update_order_json(order: Dict):
    with open(ORDER_DB_FILE, "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        try:
            current_key = int(list(data["orders"].keys())[-1]) + 1
        except (KeyError, IndexError):
            current_key = '1'
    order["order_id"] = current_key
    data["orders"][current_key] = order

    with open(ORDER_DB_FILE, "w", encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile, indent=4, ensure_ascii=False)
    return current_key


async def record_to_order_db(order: Dict):
    try:
        current_key = update_order_json(order)
    except Exception as e:
        print(e)
        create_order_json()
        current_key = update_order_json(order)
    return current_key
