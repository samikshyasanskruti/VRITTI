
from backend.app.services.simulator.score_projection import (
    project_match_score,
)


def run_what_if(
    current_score: float,
    added_skills: list[str] | None = None,
    missing_skills: list[str] | None = None,
) -> dict:
    """Compare a current score with a hypothetical skill scenario."""

    result = project_match_score(
        current_score=current_score,
        added_skills=added_skills,
        missing_skills=missing_skills,
    )

    return {
        "scenario": {
            "added_skills": added_skills or [],
            "missing_skills": missing_skills or [],
        },
        **result,
    }
