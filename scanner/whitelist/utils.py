def generate_vuln_id(file_path: str, vuln_type: str) -> str:
    clean_path = file_path.replace("/", "_").replace("\\", "_")
    return f"{clean_path}::{vuln_type.lower()}"
