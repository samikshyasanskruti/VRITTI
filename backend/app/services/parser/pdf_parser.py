
from pathlib import Path
from pypdf import PdfReader

from backend.app.services.parser.text_cleaner import clean_text


def parse_pdf(file_path: str | Path) -> str:
    """Extract text from a PDF resume."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    try:
        reader = PdfReader(str(path))
        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        text = clean_text("\n".join(pages))

        if not text:
            raise ValueError(
                "No text could be extracted from this PDF. "
                "It may be scanned and require OCR."
            )

        return text

    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Unable to parse PDF: {exc}") from exc
