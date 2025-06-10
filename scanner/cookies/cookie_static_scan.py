import os
import re
import logging
from sqlalchemy.orm import Session
from log import log_issue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USE_COOKIE_PATTERN = re.compile(r"useCookie\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*(\{[\s\S]*?\})\s*\)", re.MULTILINE)

SET_COOKIE_PATTERN = re.compile(
    r"setCookie\s*\((?:event\s*,\s*)?['\"]([^'\"]+)['\"]\s*,\s*[^,)]+\s*,\s*(\{[\s\S]*?\})\s*\)", 
    re.MULTILINE
)

DOCUMENT_COOKIE_PATTERN = re.compile(r"document\.cookie\s*=\s*([^;]+)", re.MULTILINE)

HTTP_ONLY_PATTERN = re.compile(r"httpOnly\s*:\s*true")
SECURE_PATTERN = re.compile(r"secure\s*:\s*true")
SAMESITE_PATTERN = re.compile(r"sameSite\s*:\s*['\"](strict|lax)['\"]", re.IGNORECASE)
MAX_AGE_PATTERN = re.compile(r"maxAge\s*:\s*(\d+)")