
import re

from backend.app.services.skills.skill_normalizer import normalize_skill


SKILL_ALIASES = {
    "python": ["python", "python3"],
    "machine learning": ["machine learning", "ml"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "fastapi": ["fastapi", "fast api"],
}


def extract_skills(text: str) -> list[str]:
    """Extract known skills from text using case-insensitive aliases."""
    if not text:
        return []

    normalized_text = text.lower()
    found = []

    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = (
                r"(?<![a-z0-9+#.-])"
                + re.escape(alias.lower())
                + r"(?![a-z0-9+#.-])"
            )

            if re.search(pattern, normalized_text):
                found.append(normalize_skill(canonical))
                break

    return list(dict.fromkeys(found))
