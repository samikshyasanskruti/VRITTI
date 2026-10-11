
from backend.app.services.skills.skill_normalizer import (
    normalize_skill,
    normalize_skills,
)
from backend.app.services.skills.skill_extractor import extract_skills
from backend.app.services.skills.skill_classifier import classify_skills
from backend.app.services.skills.skill_taxonomy import (
    SKILL_TAXONOMY,
    get_skill_category,
)
from backend.app.services.skills.skill_aliases import canonical_skill

__all__ = [
    "normalize_skill",
    "normalize_skills",
    "extract_skills",
    "classify_skills",
    "SKILL_TAXONOMY",
    "get_skill_category",
    "canonical_skill",
]
