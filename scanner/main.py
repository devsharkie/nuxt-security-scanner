import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from scans.pattern_detector import scan_vue_ts_files

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
        status = scan_vue_ts_files("/app/frontend", session)
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
