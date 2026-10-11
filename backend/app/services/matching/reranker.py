
def rerank_jobs(
    jobs: list[dict],
    top_k: int = 20,
) -> list[dict]:
    """Sort already-scored job matches by alignment score."""

    ranked = sorted(
        jobs,
        key=lambda job: float(job.get("score") or 0.0),
        reverse=True,
    )

    return ranked[:max(1, min(top_k, 100))]
