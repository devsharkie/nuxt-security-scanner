import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, ScanLog

# Konfiguracja bazy
DATABASE_URL = "postgresql://scanner:scanner@db:5432/scannerdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Tworzymy tabele jeśli ich nie ma
Base.metadata.create_all(engine)

# Skanowanie plików .vue w folderze frontend
def scan_vue_files():
    session = SessionLocal()
    root_dir = "/app/frontend"
    found_issue = 0

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".vue"):
                path = os.path.join(dirpath, filename)
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
    session.commit()
    session.close()
    exit(found_issue)

if __name__ == "__main__":
    scan_vue_files()
