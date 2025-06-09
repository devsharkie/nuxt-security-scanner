import os
import logging
from sqlalchemy.orm import Session
from log import log_issue
from pathlib import Path

DETECTION_PATTERNS = [
    {
        "pattern": "v-html",
        "severity": "HIGH",
        "message": "Found v-html directive"
    },
    {
        "pattern": "eval(",
        "severity": "HIGH",
        "message": "Usage of eval() detected"
    },
    {
        "pattern": ':href="userProvidedUrl"',
        "severity": "MEDIUM",
        "message": "Possible user-controlled URL injection"
    },
    {
        "pattern": ':style="userProvidedStyles"',
        "severity": "MEDIUM",
        "message": "Possible user-controlled style injection"
    },
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scan_vue_ts_files(root_dir: str, session: Session) -> int:
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
                            if rule["pattern"] in content:
                                found_issue = 1
                                log_issue(session, rule["severity"], rule["message"], path)
                                logger.warning(f"Issue found in {path}: {rule['message']}")

                except UnicodeDecodeError:
                    logger.error(f"UnicodeDecodeError in {path}")
                except Exception as e:
                    logger.error(f"Error reading {path}: {e}")

    return found_issue