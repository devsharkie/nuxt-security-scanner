from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Scan(Base):
  __tablename__ = "scans"
  id = Column(Integer, primary_key=True, index=True)
  timestamp = Column(DateTime, default=datetime.utcnow)
  result = Column(Boolean, default=False)
  logs = relationship("ScanLog", back_populates="scan")

class ScanLog(Base):
  __tablename__ = "scan_logs"
  scan_id = Column(Integer, ForeignKey("scans.id"))
  id = Column(Integer, primary_key=True, index=True)
  vuln_id = Column(String, index=True)
  timestamp = Column(DateTime, default=datetime.utcnow)
  severity = Column(String)
  message = Column(String)
  file_path = Column(String)
  scan = relationship("Scan", back_populates="logs")