import os
import re
import logging
from sqlalchemy.orm import Session
from log import log_issue
from whitelist.utils import generate_vuln_id
from whitelist.manager import is_whitelisted

DETECTION_PATTERNS = [
  { "pattern": r'v-html\s*=\s*"[^"]*"', "severity": "HIGH", "message": "Found v-html directive", "type": "v-html" },
  { "pattern": r'eval\s*\(', "severity": "HIGH", "message": "Usage of eval() detected", "type": "eval" },
  { "pattern": r':href\s*=\s*"[^"]*"', "severity": "MEDIUM", "message": "Possible user-controlled URL injection", "type": "url-injection" },
  { "pattern": r':style\s*=\s*"[^"]*"', "severity": "MEDIUM", "message": "Possible user-controlled style injection", "type": "style-injection" },
  { "pattern": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "severity": "MEDIUM", "message": "Found possibly exposed email information", "type": "email" },
  { "pattern": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', "severity": "MEDIUM", "message": "Found possibly exposed phone information", "type": "phone" },
  { "pattern": r'\b\d{3}-\d{2}-\d{4}\b', "severity": "HIGH", "message": "Found possibly exposed SSN", "type": "ssn" },
  { "pattern": r'api[_-]?key[_-]?([\'"|`])([a-zA-Z0-9]{32,45})\1', "severity": "HIGH", "message": "Found possibly exposed API key", "type": "apikey" },
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scan_vue_ts_files(root_dir: str, session: Session, scan_id: int) -> int:
  found_issue = 0
  logger.info(f"Starting scan in directory: {root_dir}")

  if not os.path.exists(root_dir):
    logger.error(f"Directory '{root_dir}' does not exist.")
    return 1

  for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".nuxt", "dist"}]
    for filename in filenames:
      if filename.endswith((".vue", ".ts")):
        path = os.path.join(dirpath, filename)
        logger.info(f"Scanning file: {path}")
        try:
          with open(path, encoding="utf-8") as f:
            content = f.read()
                        
            for rule in DETECTION_PATTERNS:
              if re.search(rule["pattern"], content):           
               
                vuln_id = generate_vuln_id(str(path), rule["type"])
                if not is_whitelisted(vuln_id):
                  log_issue(session=session, severity=rule["severity"], message=rule["message"], file_path=path, vuln_id=vuln_id, scan_id=scan_id)
                  logger.warning(f"Issue found in {path}: {rule['message']}")
                  found_issue = 1

        except UnicodeDecodeError:
          logger.error(f"UnicodeDecodeError in {path}")
        except Exception as e:
          logger.error(f"Error reading {path}: {e}")

  return found_issue