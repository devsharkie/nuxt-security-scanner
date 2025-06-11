import requests
import logging
import base64 
from sqlalchemy.orm import Session
from log import log_issue
from whitelist.manager import is_whitelisted
from whitelist.utils import generate_vuln_id
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://frontend:3000/api"
HEADERS = {'Content-Type': 'application/json'}

# HARDCODED TEST USERS
TEST_USERS = {
  "user": {"username": "user", "password": "password123", "expected_role": "user"},
  "admin": {"username": "admin", "password": "supersecretpassword", "expected_role": "admin"},
  "user_test": {"username": "user_test", "password": "testpassword", "expected_role": "user"}
}

def get_basic_auth_header(username: str, password: str) -> Dict[str, str]:
  credentials = f"{username}:{password}"
  encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
  return {'Authorization': f'Basic {encoded_credentials}'}

ACCESS_CONTROL_TESTS = [
  {"name": "Unauthenticated access to /logged", "endpoint": "/logged", "method": "GET", "auth_type": "none", "expected_status": 401, "expected_message_part": "Unauthorized"},
  {"name": "Unauthenticated access to /admin", "endpoint": "/admin", "method": "GET", "auth_type": "none", "expected_status": 401, "expected_message_part": "Unauthorized"},

  {"name": "User access to /logged (expected success)", "endpoint": "/logged", "method": "GET", "auth_type": "user", "expected_status": 200, "expected_message_part": "Welcome, user"},
  {"name": "User access to /admin (expected forbidden)", "endpoint": "/admin", "method": "GET", "auth_type": "user", "expected_status": 403, "expected_message_part": "Forbidden"},

  {"name": "User_test access to /logged (expected success)", "endpoint": "/logged", "method": "GET", "auth_type": "user_test", "expected_status": 200, "expected_message_part": "Welcome, user_test"},
  {"name": "User_test access to /admin (expected forbidden)", "endpoint": "/admin", "method": "GET", "auth_type": "user_test", "expected_status": 403, "expected_message_part": "Forbidden"},

  {"name": "Admin access to /logged (expected success)", "endpoint": "/logged", "method": "GET", "auth_type": "admin", "expected_status": 200, "expected_message_part": "Welcome, admin"},
  {"name": "Admin access to /admin (expected success)", "endpoint": "/admin", "method": "GET", "auth_type": "admin", "expected_status": 200, "expected_message_part": "Welcome, Admin"},

  {
    "name": "Attempt admin login via public /api/login (expected forbidden)", 
    "endpoint": "/login", 
    "method": "POST",
    "auth_type": "none", 
    "expected_status": 401,
    "payload_override": {"username": "admin", "password": "supersecretpassword"},
    "expected_message_part": "Invalid credentials"
  },

  {
    "name": "Successful admin login via /api/admin-login", 
    "endpoint": "/admin-login", 
    "method": "POST",
    "auth_type": "none", 
    "expected_status": 200,
    "payload_override": {"username": "admin", "password": "supersecretpassword"},
    "expected_message_part": "Admin login successful"
  },

  {
    "name": "Attempt user login via /api/admin-login (expected forbidden)", 
    "endpoint": "/admin-login", 
    "method": "POST",
    "auth_type": "none", 
    "expected_status": 403,
    "payload_override": {"username": "user", "password": "password123"},
    "expected_message_part": "Forbidden"
  },

  # login role manipulation
  {
    "name": "Attempt login as user with admin role in payload (POST /login)", 
    "endpoint": "/login", 
    "method": "POST",
    "auth_type": "none", 
    "expected_status": 200, 
    "payload_override": {"username": "user", "password": "password123", "role": "admin"},
    "post_login_check": {"field": "role", "expected_value": "user", "failure_message": "User was able to gain admin role via login payload."}
  },
  
  {
    "name": "Attempt login as non-existent admin user (POST /login)", 
    "endpoint": "/login", 
    "method": "POST",
    "auth_type": "none", 
    "expected_status": 401, 
    "payload_override": {"username": "eviladmin", "password": "password", "role": "admin"},
    "expected_message_part": "Invalid credentials"
  },
]

def run_access_control_audit(root_dir: str, session: Session, scan_id: int) -> int:
    found_issue = 0

    for test_case in ACCESS_CONTROL_TESTS:
        test_name = test_case["name"]
        endpoint = test_case["endpoint"]
        method = test_case["method"]
        auth_type = test_case["auth_type"]
        expected_status = test_case["expected_status"]
        expected_message_part = test_case.get("expected_message_part")
        payload_override = test_case.get("payload_override")
        post_login_check = test_case.get("post_login_check")

        logger.info(f"Running test: {test_name}")

        request_headers = HEADERS.copy()
        current_payload = None

        if endpoint not in ["/login", "/admin-login"] and auth_type != "none":
            user_creds = TEST_USERS.get(auth_type)
            if not user_creds:
                logger.warning(f"Skipping test '{test_name}' due to missing credentials for '{auth_type}'.")
                found_issue = 1
                continue 
            request_headers.update(get_basic_auth_header(user_creds["username"], user_creds["password"]))

        if payload_override:
            current_payload = payload_override
        elif method == "POST": 
            current_payload = {}

        try:
            response = requests.request(method, f"{BASE_URL}{endpoint}", json=current_payload, headers=request_headers, timeout=10)

            response_data = None
            try:
                response_data = response.json()
            except requests.exceptions.JSONDecodeError:
                response_data = response.text # Fallback to text if not JSON

            is_test_passing = True

            # 1. Check HTTP Status Code
            if response.status_code != expected_status:
                is_test_passing = False
                message = ( f"Test '{test_name}' FAILED: " f"Expected {expected_status}, got {response.status_code}. " f"Response: {response_data}")
                logger.error(message)
            else:
                logger.info(f"Test '{test_name}' got expected {response.status_code}")

            # 2. Check Expected Message Part 
            if is_test_passing and expected_message_part:
                response_content = str(response_data) 
                if expected_message_part not in response_content:
                    is_test_passing = False
                    message = ( f"Test '{test_name}' FAILED: " f"'{expected_message_part}' not found in response. " f"Response: {response_data}")
                    logger.error(message)
                else:
                    logger.info(f"Test '{test_name}' Message OK: Found expected message part.")

            # 3. Post-login check for role manipulation
            if is_test_passing and post_login_check and endpoint in ["/login", "/admin-login"]:
                field = post_login_check["field"]
                expected_value = post_login_check["expected_value"]
                failure_message = post_login_check["failure_message"]

                actual_value = None
                if isinstance(response_data, dict):
                    user_data = response_data.get("user")
                    if isinstance(user_data, dict):
                        actual_value = user_data.get(field)

                if actual_value != expected_value:
                    is_test_passing = False
                    message = f"Test '{test_name}' FAILED: {failure_message} Actual '{field}': {actual_value}"
                    logger.error(message)
                else:
                    logger.info(f"Test '{test_name}' Post-Login Check OK: '{field}' is '{actual_value}' as expected.")

            if not is_test_passing:
                found_issue = 1
                vuln_id = generate_vuln_id(f"access_control:{endpoint}:{method}:{auth_type}", "ACCESS-C-001")
                if not is_whitelisted(vuln_id):
                    log_issue(session=session, scan_id=scan_id, severity="HIGH", message=f"Access Control Violation: Test '{test_name}' failed. {message}",
                              file_path=f"api{endpoint}", vuln_id=vuln_id)

        except requests.exceptions.RequestException as e:
            logger.error(f"Critical error during test '{test_name}': {e}")
            found_issue = 1

    return found_issue