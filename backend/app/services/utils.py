import os, uuid
from pathlib import Path
from typing import Optional
from pdfminer.high_level import extract_text as pdf_extract_text
import docx2txt

BASE_STORAGE = Path(os.getenv("STORAGE_PATH", "/tmp/ai_workspace_storage"))
BASE_STORAGE.mkdir(parents=True, exist_ok=True)

def save_uploaded_file(upload_file, subdir: str = "uploads") -> str:
    dest_dir = BASE_STORAGE / subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(upload_file.filename).suffix or ""
    filename = f"{uuid.uuid4().hex}{ext}"
    dest_path = dest_dir / filename
    with open(dest_path, "wb") as out:
        content = upload_file.file.read()
        out.write(content)
    return str(dest_path)

def extract_text_from_file(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() in [".pdf"]:
        try:
            return pdf_extract_text(str(p))
        except Exception as e:
            print("pdf extract error:", e)
            return ""
    if p.suffix.lower() in [".docx", ".doc"]:
        try:
            return docx2txt.process(str(p)) or ""
        except Exception as e:
            print("docx extract error:", e)
            return ""
    # fallback: try read as text
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
