from .loader import load_whitelist

_whitelist_cache = load_whitelist()

def is_whitelisted(vuln_id: str) -> bool:
  return vuln_id in _whitelist_cache
