
from pathlib import Path

from backend.app.services.parser.pdf_parser import parse_pdf
from backend.app.services.parser.docx_parser import parse_docx
from backend.app.services.parser.text_cleaner import clean_text
from backend.app.services.resume.profile_extractor import (
    extract_profile,
)
from backend.app.services.resume.section_detector import detect_sections
from backend.app.services.resume.project_extractor import extract_projects


def parse_resume(file_path: str | Path) -> dict:
    """Parse PDF, DOCX, or TXT resumes into a structured profile."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume file not found: {path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        raw_text = parse_pdf(path)
    elif extension == ".docx":
        raw_text = parse_docx(path)
    elif extension == ".txt":
        raw_text = path.read_text(encoding="utf-8", errors="replace")
    else:
        raise ValueError("Supported resume formats are PDF, DOCX, and TXT.")

    text = clean_text(raw_text)

    if not text:
        raise ValueError("No readable text was found in the resume.")

    profile = extract_profile(text)
    profile["sections"] = detect_sections(text)
    profile["projects"] = extract_projects(text)
    profile["text"] = text

    return profile
