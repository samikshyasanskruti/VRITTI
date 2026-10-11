
from collections import Counter


def recommend_careers(
    resume_profile: dict,
    job_matches: list[dict] | None = None,
    top_k: int = 5,
) -> list[dict]:
    """Recommend career areas based on skills and retrieved job matches."""

    skills = {
        str(skill).strip().lower()
        for skill in (resume_profile.get("skills") or [])
        if str(skill).strip()
    }

    jobs = job_matches or []
    career_counts = Counter()
    career_examples = {}

    for job in jobs:
        title = str(job.get("title") or "").strip()
        if not title:
            continue

        career_counts[title] += 1
        career_examples.setdefault(title, job)

    recommendations = []

    for title, count in career_counts.most_common(max(1, top_k)):
        example = career_examples[title]
        recommendations.append({
            "career_title": title,
            "company_example": example.get("company"),
            "matching_jobs_in_results": count,
            "resume_skills": sorted(skills),
            "reason": (
                "This role appeared in the retrieved job matches. "
                "Review the job description and skill requirements "
                "before deciding whether it suits your career goals."
            ),
        })

    return recommendations
