
SKILL_ALIASES = {
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "postgres": "postgresql",
    "scikit learn": "scikit-learn",
    "powerbi": "power bi",
    "aws": "amazon web services",
    "gcp": "google cloud platform",
}


def canonical_skill(skill: str) -> str:
    value = str(skill or "").strip().lower()
    return SKILL_ALIASES.get(value, value)
