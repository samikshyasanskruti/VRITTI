
from backend.app.services.parser.text_cleaner import clean_text


def parse_job_description(job: dict) -> dict:
    """Normalize a job posting into a consistent structure."""

    title = str(job.get("title") or "").strip()
    description = clean_text(
        str(job.get("description") or job.get("job_description") or "")
    )

    return {
        "external_id": str(
            job.get("external_id") or job.get("source_id") or ""
        ),
        "title": title,
        "company": str(job.get("company") or "").strip(),
        "location": str(job.get("location") or "").strip(),
        "description": description,
        "source_url": job.get("source_url"),
        "skills_desc": clean_text(str(job.get("skills_desc") or "")),
    }
