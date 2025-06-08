import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ScanLog
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfiguracja bazy
DATABASE_URL = "postgresql://scanner:scanner@db:5432/scannerdb"
engine = None # Initialize outside try-block
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    logger.info("Successfully created SQLAlchemy engine.")
except Exception as e:
    logger.error(f"Error connecting to database: {e}")
    exit(1) # Exit if database connection fails

# Tworzymy tabele jeśli ich nie ma
try:
    Base.metadata.create_all(engine)
    logger.info("Successfully created database tables (if not existing).")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")
    exit(1)

# Skanowanie plików .vue w folderze frontend
def scan_vue_files():
    session = SessionLocal()
    root_dir = "/app/frontend"
    found_issue = 0
    logger.info(f"Starting scan in directory: {root_dir}")

    if not os.path.exists(root_dir):
        logger.error(f"Frontend directory '{root_dir}' does not exist.")
        session.close()
        exit(1)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".vue"):
                path = os.path.join(dirpath, filename)
                logger.info(f"Scanning file: {path}")
                try:
                    with open(path, encoding="utf-8") as f:
                        content = f.read()
                        if "v-html" in content:
                            found_issue = 1
                            log = ScanLog(
                                severity="HIGH",
                                message="Found v-html directive",
                                file_path=path
                            )
                            session.add(log)
                            logger.warning(f"Issue found in {path}: 'v-html' directive.")
                except UnicodeDecodeError:
                    logger.error(f"UnicodeDecodeError when reading file: {path}. Check file encoding.")
                except Exception as e:
                    logger.error(f"Error processing file {path}: {e}")

    try:
        session.commit()
        logger.info("Changes committed to database.")
    except Exception as e:
        logger.error(f"Error committing to database: {e}")
        found_issue = 1 # Mark as an issue if commit fails
    finally:
        session.close()
        logger.info("Session closed.")

    logger.info(f"Scan finished. Exiting with status: {found_issue}")
    exit(found_issue)

if __name__ == "__main__":
    scan_vue_files()