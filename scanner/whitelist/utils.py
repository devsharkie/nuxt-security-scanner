def generate_id(vuln_type: str, file_path: str, detail: str) -> str:
    return f"{vuln_type}::{file_path}::{detail}"
