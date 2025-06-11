import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from scans.pattern_detector import scan_vue_ts_files
from cookies.cookie_static_scan import cookie_static_scan
from log import log_session
from sqlinjection.sqli_runtime_audit import run_test

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
        status |= scan_vue_ts_files("/app/frontend", session, scan_id=scan_id)
        status |= cookie_static_scan("/app/frontend", session, scan_id=scan_id)
        sql_injection_payload = {"username": "' OR 1=1 --"}
        run_test(
        "Atak na podatny endpoint (notsecure_sqli)",
        f"http://frontend:3000/api/notsecure_sqli",
        sql_injection_payload,
        is_attack_expected_to_succeed=True
    )
        run_test(
        "Atak na bezpieczny endpoint (secure_sqli)",
        f"http://frontend:3000/api/secure_sqli",
        sql_injection_payload,
        is_attack_expected_to_succeed=False
    )
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

# curl -v -X POST -H "Content-Type: application/json" -d '{"username": "testuser"}' http://localhost:3000/api/notsecure_sqli
# Note: Unnecessary use of -X or --request, POST is already inferred.
# * Host localhost:3000 was resolved.
# * IPv6: ::1
# * IPv4: 127.0.0.1
# *   Trying [::1]:3000...
# * Connected to localhost (::1) port 3000
# > POST /api/notsecure_sqli HTTP/1.1
# > Host: localhost:3000
# > User-Agent: curl/8.5.0
# > Accept: */*
# > Content-Type: application/json
# > Content-Length: 24
# > 
# < HTTP/1.1 200 OK
# < content-type: application/json
# < date: Wed, 11 Jun 2025 00:48:47 GMT
# < connection: close
# < content-length: 130
# < 
# {
#   "error": "SQLITE_ERROR: no such table: users",
#   "query": "SELECT id, username, role FROM users WHERE username = 'testuser'"
# * Closing connection