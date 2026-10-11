
import re


def normalize_skill(skill: str) -> str:
    """Normalize skill spelling and whitespace."""
    value = re.sub(r"\s+", " ", str(skill or "").strip().lower())

    aliases = {
        "py": "python",
        "js": "javascript",
        "ml": "machine learning",
        "dl": "deep learning",
        "nlp": "natural language processing",
        "postgres": "postgresql",
        "scikit learn": "scikit-learn",
        "powerbi": "power bi",
    }

    return aliases.get(value, value)


def normalize_skills(skills: list[str]) -> list[str]:
    """Normalize and deduplicate skills."""
    result = []
    seen = set()

    for skill in skills or []:
        normalized = normalize_skill(skill)
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)

    return result
