from pathlib import Path
ALLOWED_RESUME_EXTENSIONS={".pdf",".docx",".txt"}
def valid_resume_filename(filename): return Path(filename or "").suffix.lower() in ALLOWED_RESUME_EXTENSIONS
