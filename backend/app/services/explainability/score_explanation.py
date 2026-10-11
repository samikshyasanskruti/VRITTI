
def explain_score(match: dict) -> dict:
    """Describe the available ranking scores without overstating certainty."""
    score = match.get("score")
    similarity = match.get("semantic_similarity")
    coverage = match.get("required_coverage")

    components = {
        "alignment_score": score,
        "semantic_similarity": similarity,
        "required_skill_coverage": (
            round(coverage * 100, 2)
            if isinstance(coverage, (int, float))
            else None
        ),
    }

    if coverage is None:
        note = (
            "Required-skill coverage is unavailable or not calculated. "
            "The alignment score should not be interpreted as hiring probability."
        )
    else:
        note = (
            "The score summarizes resume-job alignment. "
            "It does not predict whether an employer will hire the candidate."
        )

    return {
        "components": components,
        "explanation": note,
    }
