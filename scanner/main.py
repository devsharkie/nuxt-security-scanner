import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from scans.pattern_detector import scan_vue_ts_files
from cookies.cookie_static_scan import cookie_static_scan
from log import log_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://scanner:scanner@db:5432/scannerdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def main():
    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables ensured.")
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        exit(1)

    session = SessionLocal()
    try:
        scan_id = log_session(session)
        status = scan_vue_ts_files("/app/frontend", session, scan_id=scan_id)
        cookie_status = cookie_static_scan("/app/frontend", session, scan_id=scan_id)
        if status == 0 and cookie_status == 1:
            status = 1
        session.commit()
    except Exception as e:
        logger.error(f"Scan error: {e}")
        status = 1
    finally:
        session.close()

    logger.info(f"Scan complete. Exit status: {status}")
    exit(status)

if __name__ == "__main__":
    main()
