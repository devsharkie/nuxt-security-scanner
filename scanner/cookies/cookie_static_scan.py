import os
import re
import logging
from sqlalchemy.orm import Session
from log import log_issue
from whitelist.utils import generate_vuln_id

MAX_COOKIE_EXPIRATION_DAYS = 90

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USE_COOKIE_PATTERN = re.compile(r"useCookie\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*(\{[\s\S]*?\})\s*\)", re.MULTILINE)
SET_COOKIE_PATTERN = re.compile(r"setCookie\s*\((?:event\s*,\s*)?['\"]([^'\"]+)['\"]\s*,\s*[^,)]+\s*,\s*(\{[\s\S]*?\})\s*\)", re.MULTILINE)
DOCUMENT_COOKIE_PATTERN = re.compile(r"document\.cookie\s*=\s*([^;]+)", re.MULTILINE)

HTTP_ONLY_PATTERN = re.compile(r"httpOnly\s*:\s*true")
SECURE_PATTERN = re.compile(r"secure\s*:\s*true")
SAMESITE_PATTERN = re.compile(r"sameSite\s*:\s*['\"](strict|lax)['\"]", re.IGNORECASE)
MAX_AGE_PATTERN = re.compile(r"maxAge\s*:\s*(\d+)")

COOKIE_RULES = [
  {"pattern": HTTP_ONLY_PATTERN, "severity": "LOW", "message": "Cookie missing httpOnly", "type": "httpOnly", "missing_check": True},
  {"pattern": SECURE_PATTERN, "severity": "MEDIUM", "message": "Cookie missing secure", "type": "secure", "missing_check": True},
  {"pattern": SAMESITE_PATTERN, "severity": "LOW", "message": "Cookie missing samesite", "type": "samesite", "missing_check": True},
  {"pattern": MAX_AGE_PATTERN, "severity": "MEDIUM", "message": "Cookie expires in", "type": "max-age",  "custom_check": lambda m: int(m.group(1)) > MAX_COOKIE_EXPIRATION_DAYS * 86400, "custom_days": lambda m: int(m.group(1)) / (60 * 60 * 24)},
]

def analyze_cookie_options(options_block: str, cookie_name: str, file_path: str, session: Session, scan_id: int):
  base_id = f"{file_path}:{cookie_name}"

  if not HTTP_ONLY_PATTERN.search(options_block):
    log_issue(session=session, severity='LOW',
              message=f"Ciasteczko '{cookie_name}' prawdopodobnie nie ma flagi 'httpOnly' (lub jest ustawiane na kliencie).",
              file_path=file_path,
              vuln_id=generate_vuln_id(base_id, "httpOnly"),
              scan_id=scan_id)
    logger.warning(f"Issue found in {file_path}: {base_id}")

  if not SECURE_PATTERN.search(options_block):
    log_issue(session=session, severity='MEDIUM',
              message=f"Ciasteczko '{cookie_name}' prawdopodobnie nie ma flagi 'secure'.",
              file_path=file_path,
              vuln_id=generate_vuln_id(base_id, "secure"),
              scan_id=scan_id)
    logger.warning(f"Issue found in {file_path}: {base_id}")

  if not SAMESITE_PATTERN.search(options_block):
    log_issue(session=session, severity='LOW',
              message=f"Ciasteczko '{cookie_name}' nie ma restrykcyjnej polityki 'sameSite' ('lax' lub 'strict').",
              file_path=file_path,
              vuln_id=generate_vuln_id(base_id, "samesite"),
              scan_id=scan_id)
    logger.warning(f"Issue found in {file_path}: {base_id}")

  max_age_match = MAX_AGE_PATTERN.search(options_block)
  if max_age_match:
    max_age_seconds = int(max_age_match.group(1))
    max_age_days = max_age_seconds / (60 * 60 * 24)
    if max_age_days > MAX_COOKIE_EXPIRATION_DAYS:
      log_issue(session=session, severity='MEDIUM',
                message=f"Ciasteczko '{cookie_name}' ma bardzo długi czas życia: {int(max_age_days)} dni.",
                file_path=file_path,
                vuln_id=generate_vuln_id(base_id, "max-age"),
                scan_id=scan_id)
      logger.warning(f"Issue found in {file_path}: {base_id}")

def analyze_use_cookie(content: str, file_path: str, session: Session, scan_id: int):
    matches = USE_COOKIE_PATTERN.finditer(content)
    for match in matches:
        cookie_name, options_block = match.groups()
        analyze_cookie_options(options_block, cookie_name, file_path, session, scan_id)

def analyze_set_cookie(content: str, file_path: str, session: Session, scan_id: int):
    matches = SET_COOKIE_PATTERN.finditer(content)
    for match in matches:
        cookie_name, options_block = match.groups()
        analyze_cookie_options(options_block, cookie_name, file_path, session, scan_id)

def analyze_document_cookie(content: str, file_path: str, session: Session, scan_id: int):
    matches = DOCUMENT_COOKIE_PATTERN.finditer(content)
    for match in matches:
        cookie_assignment = match.group(1).lower()
        base_id = f"{file_path}:document.cookie"
        
        if '+' in match.group(0):
            log_issue(session=session, severity='HIGH',
                      message="Wykryto potencjalnie niebezpieczne przypisanie do `document.cookie` z użyciem zmiennej. Wymaga to ręcznej weryfikacji.",
                      file_path=file_path,
                      vuln_id=generate_vuln_id(base_id, "dynamic-cookie"),
                      scan_id=scan_id)
            logger.warning(f"Issue found in {file_path}: {base_id}")

        if 'httponly' not in cookie_assignment:
            log_issue(session=session, severity='HIGH',
                      message="W `document.cookie` nie można ustawić flagi 'httpOnly' z poziomu JavaScript.",
                      file_path=file_path,
                      vuln_id=generate_vuln_id(base_id, "httponly-client"),
                      scan_id=scan_id)
            logger.warning(f"Issue found in {file_path}: {base_id}")

        if 'secure' not in cookie_assignment:
            log_issue(session=session, severity='MEDIUM',
                      message="Brak flagi 'secure' w `document.cookie`.",
                      file_path=file_path,
                      vuln_id=generate_vuln_id(base_id, "secure-client"),
                      scan_id=scan_id)
            logger.warning(f"Issue found in {file_path}: {base_id}")

        if 'samesite' not in cookie_assignment:
            log_issue(session=session, severity='LOW',
                      message="Brak polityki 'sameSite' w `document.cookie`.",
                      file_path=file_path,
                      vuln_id=generate_vuln_id(base_id, "samesite-client"),
                      scan_id=scan_id)
            logger.warning(f"Issue found in {file_path}: {base_id}")

def cookie_static_scan(root_dir: str, session: Session, scan_id: int) -> int:
    found_issue = 0
    logger.info(f"Rozpoczynanie analizy ciasteczek w katalogu: {root_dir}")

    if not os.path.exists(root_dir):
        logger.error(f"Katalog '{root_dir}' nie istnieje.")
        return 1

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".nuxt", "dist"}]

        for filename in filenames:
            if filename.endswith((".vue", ".ts")):
                file_path = os.path.join(dirpath, filename)
                logger.info(f"Analiza pliku: {file_path}")
                try:
                    with open(file_path, encoding="utf-8") as f:
                        content = f.read()

                        before = len(session.dirty) + len(session.new)  # Liczba zgłoszonych błędów przed
                        analyze_use_cookie(content, file_path, session, scan_id)
                        analyze_set_cookie(content, file_path, session, scan_id)
                        analyze_document_cookie(content, file_path, session, scan_id)
                        after = len(session.dirty) + len(session.new)

                        if after > before:
                            found_issue = 1

                except UnicodeDecodeError:
                    logger.warning(f"Problem z kodowaniem pliku: {file_path}")
                except Exception as e:
                    logger.error(f"Błąd podczas analizy {file_path}: {e}")

    return found_issue