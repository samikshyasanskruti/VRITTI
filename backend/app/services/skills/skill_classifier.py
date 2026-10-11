
from backend.app.services.skills.skill_taxonomy import get_skill_category


def classify_skills(skills: list[str]) -> dict[str, list[str]]:
    """Group detected skills into taxonomy categories."""

    result = {}

    for skill in skills or []:
        category = get_skill_category(skill)
        result.setdefault(category, []).append(skill)

    return result
