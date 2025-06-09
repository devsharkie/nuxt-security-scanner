import os
import re
import logging
from sqlalchemy.orm import Session
from log import log_issue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)