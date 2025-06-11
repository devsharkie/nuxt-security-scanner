import requests
import time
import logging
from whitelist.utils import generate_vuln_id
from whitelist.manager import is_whitelisted
from sqlalchemy.orm import Session
from log import log_issue
from typing import List, Dict, Any, Optional

time.sleep(10)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://frontend:3000/api"
HEADERS = {'Content-Type': 'application/json'}
SQL_INJECTION_PAYLOAD = {"username": "' OR 1=1 --"}

def test_sqli(endpoint_name: str) -> Optional[List[Dict[str, Any]]]:
  url = f"{BASE_URL}/{endpoint_name}"
  logger.info(f"Testing endpoint: {endpoint_name}")

  try:
    response = requests.post(url, json=SQL_INJECTION_PAYLOAD, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data = response.json()
    users_found = data.get("data")
    logger.debug(f"Response from {endpoint_name}: {data}")
    return users_found
  
  except requests.exceptions.RequestException as e:
    logger.error(f"Error testing {endpoint_name}: {e}")


def sqli_results(root_dir: str, session: Session, scan_id: int, endpoints_to_test: List[str]) -> int:
  found_issue = 0

  for endpoint in endpoints_to_test:
    test_result=test_sqli(endpoint)

    if test_result is None:
      logger.error(f"Could not complete test for '{endpoint}'. Check connectivity and server logs.")
      found_issue = 1
      continue

    if isinstance(test_result, list) and len(test_result) > 0:
      vuln_id = generate_vuln_id(str("api/{endpoint}"), "SQLI-001")
      if not is_whitelisted(vuln_id):
        message = f"Endpoint '{endpoint}' is vulnerable to SQL Injection. Returned {len(test_result)} users."
        logger.warning(message)
        log_issue(session=session, scan_id=scan_id, severity="HIGH", message=message, file_path=f"api/{endpoint}", vuln_id=vuln_id)
        found_issue = 1

    elif isinstance(test_result, list) and len(test_result) == 0:
      logger.info(f"Endpoint '{endpoint}' behaved securely against SQL injection.")

    else:
      message = f"Endpoint '{endpoint}' returned an unexpected data format or error during test."
      log_issue(session=session, scan_id=scan_id, severity="MEDIUM", message=message, file_path=f"api/{endpoint}", vuln_id="SQLI-UNEXPECTED-RES")
      found_issue = 1

  return found_issue