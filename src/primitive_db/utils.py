import json
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "data")
META_FILE = os.path.join(os.path.dirname(__file__), "db_meta.json")

os.makedirs(BASE_DIR, exist_ok=True)


def load_metadata():
    try:
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(data):
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_table_data(table_name):
    path = os.path.join(BASE_DIR, f"{table_name}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    path = os.path.join(BASE_DIR, f"{table_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
