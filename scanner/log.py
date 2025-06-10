from sqlalchemy.orm import Session
from models import ScanLog, Scan, HeaderScan
from datetime import datetime

def log_issue(session: Session, scan_id: int, severity: str, message: str, file_path: str, vuln_id: str):
  log = ScanLog(
    scan_id=scan_id,
    vuln_id=vuln_id,
    severity=severity, 
    message=message, 
    file_path=file_path
    )
  session.add(log)

def log_session(session: Session, result: bool = True) -> int:
  scan = Scan(result=result)
  session.add(scan)
  session.commit()
  return scan.id

def log_header(session, scan_id: int, header_name: str, header_value: str, vuln_id: str):
  entry = HeaderScan(
    scan_id=scan_id,
    header_name=header_name,
    header_value=header_value,
    vuln_id=vuln_id,
    )
  session.add(entry)