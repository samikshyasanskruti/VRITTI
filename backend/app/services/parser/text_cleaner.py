
import re
import html


def clean_text(text: str) -> str:
    """Clean extracted resume or job-description text."""
    if not text:
        return ""

    text = html.unescape(text)
    text = text.replace("\x00", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]*\n+", "\n\n", text)
    text = re.sub(r"[^\S\n]+", " ", text)

    return text.strip()


def normalize_text(text: str) -> str:
    """Normalize text for matching and comparison."""
    return clean_text(text).lower()


def remove_urls(text: str) -> str:
    """Remove URLs from text."""
    if not text:
        return ""

    return re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text,
        flags=re.IGNORECASE,
    ).strip()
