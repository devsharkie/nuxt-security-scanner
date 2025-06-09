import os
import logging
from sqlalchemy.orm import Session
from log import log_issue
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scan_vue_ts_files(root_dir: str, session: Session) -> int:
    found_issue = 0
    logger.info(f"Starting scan in directory: {root_dir}")

    if not os.path.exists(root_dir):
        logger.error(f"Directory '{root_dir}' does not exist.")
        return 1

    for dirpath, dirnames, filenames in os.walk(root_dir):
        relative_parts = Path(os.path.relpath(dirpath, root_dir)).parts
        # Pomijamy node_modules
        if "node_modules" in relative_parts:
            continue

        for filename in filenames:
            if filename.endswith((".vue", ".ts")):
                path = os.path.join(dirpath, filename)
                logger.info(f"Scanning file: {path}")
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()

                        if "v-html" in content:
                            found_issue = 1
                            log_issue(session, "HIGH", "Found v-html directive", path)
                            logger.warning(f"Issue found in {path}: 'v-html' directive.")

                except UnicodeDecodeError:
                    logger.error(f"UnicodeDecodeError in {path}")
                except Exception as e:
                    logger.error(f"Error reading {path}: {e}")

    return found_issue