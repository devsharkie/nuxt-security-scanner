import json
import os

WHITELIST_PATH = os.path.join(os.path.dirname(__file__), "whitelist.json")

def load_whitelist():
    if not os.path.exists(WHITELIST_PATH):
        return set()
    with open(WHITELIST_PATH, "r") as f:
        data = json.load(f)
        return set(data.get("ignored_ids", []))
