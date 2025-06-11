import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from scans.pattern_detector import scan_vue_ts_files
from cookies.cookie_static_scan import cookie_static_scan
from middleware.access_control_audit import run_access_control_audit
from log import log_session
from sqlinjection.sqli_runtime_audit import sqli_results

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://scanner:scanner@db:5432/scannerdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def main():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        exit(1)

    session = SessionLocal()
    try:
        scan_id = log_session(session)
        status = 0
        # tutaj zrob wywolanie funkcji i jako array zbieraj wyniki a nastepnie sprawdz czy chociaz jedna 1 wystepuje
        status |= scan_vue_ts_files("/app/frontend", session, scan_id=scan_id)
        status |= cookie_static_scan("/app/frontend", session, scan_id=scan_id)
        status |= sqli_results(root_dir="/app/frontend", session=session, scan_id=scan_id, endpoints_to_test=["notsecure_sqli", "secure_sqli"])
        run_access_control_audit(root_dir="/app/frontend", session=session, scan_id=scan_id)
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