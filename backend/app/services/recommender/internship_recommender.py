
def recommend_internships(
    resume_profile: dict,
    job_matches: list[dict] | None = None,
    top_k: int = 10,
) -> list[dict]:
    """Filter retrieved postings whose titles indicate internships."""

    internship_terms = (
        "intern",
        "internship",
        "trainee",
        "student placement",
        "co-op",
    )

    candidates = []

    for job in job_matches or []:
        title = str(job.get("title") or "").strip()

        if not title:
            continue

        if any(term in title.lower() for term in internship_terms):
            candidates.append({
                "job_id": job.get("job_id", job.get("id")),
                "title": title,
                "company": job.get("company"),
                "location": job.get("location"),
                "score": job.get("score"),
                "matched_skills": job.get("matched_skills", []),
                "description": job.get("description", ""),
                "source": "Retrieved job posting",
            })

    candidates.sort(
        key=lambda item: float(item.get("score") or 0),
        reverse=True,
    )

    return candidates[:max(1, min(top_k, 100))]
