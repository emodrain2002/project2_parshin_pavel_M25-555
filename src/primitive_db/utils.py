import json
import os

from .constants import BASE_DIR, META_FILE

os.makedirs(BASE_DIR, exist_ok=True)


def load_metadata():
    """Loads metadata from file."""
    try:
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(data):
    """Saves metadata to file"""
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_table_data(table_name):
    """Loads table data from file"""
    path = os.path.join(BASE_DIR, f"{table_name}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Saves table data to file."""
    path = os.path.join(BASE_DIR, f"{table_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
