
import re

from backend.app.services.skills.skill_normalizer import normalize_skill
from backend.app.services.skills.skill_taxonomy import SKILL_TAXONOMY


ALL_KNOWN_SKILLS = sorted({
    skill
    for skills in SKILL_TAXONOMY.values()
    for skill in skills
}, key=len, reverse=True)


def extract_skills(text: str) -> list[str]:
    """Extract explicitly mentioned skills from text using a small taxonomy."""
    if not text:
        return []

    found = []

    for skill in ALL_KNOWN_SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, flags=re.IGNORECASE):
            found.append(normalize_skill(skill))

    return list(dict.fromkeys(found))
