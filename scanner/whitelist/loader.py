import json
import os

WHITELIST_PATH = os.path.join(os.path.dirname(__file__), "whitelist.json")

def load_whitelist():
    try:
        with open(WHITELIST_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            return set(data.get("ignored_ids", []))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

IGNORED_IDS = load_whitelist()

def is_whitelisted(vuln_id: str) -> bool:
    return vuln_id in IGNORED_IDS
