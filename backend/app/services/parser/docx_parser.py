
from pathlib import Path
from docx import Document

from backend.app.services.parser.text_cleaner import clean_text


def parse_docx(file_path: str | Path) -> str:
    """Extract paragraphs and table text from a DOCX resume."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"DOCX file not found: {path}")

    try:
        document = Document(str(path))
        parts = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                parts.append(paragraph.text)

        for table in document.tables:
            for row in table.rows:
                values = [
                    cell.text.strip()
                    for cell in row.cells
                    if cell.text.strip()
                ]
                if values:
                    parts.append(" | ".join(values))

        text = clean_text("\n".join(parts))

        if not text:
            raise ValueError("No text could be extracted from this DOCX.")

        return text

    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Unable to parse DOCX: {exc}") from exc
