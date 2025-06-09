from sqlalchemy.orm import Session
from models import ScanLog

def log_issue(session: Session, severity: str, message: str, file_path: str):
  log = ScanLog(severity=severity, message=message, file_path=file_path)
  session.add(log)