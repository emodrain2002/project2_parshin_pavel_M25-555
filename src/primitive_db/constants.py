import os

SUPPORTED_TYPES = {"int", "str", "bool"}
BASE_DIR = os.path.join(os.path.dirname(__file__), "data")
META_FILE = os.path.join(os.path.dirname(__file__), "db_meta.json")
