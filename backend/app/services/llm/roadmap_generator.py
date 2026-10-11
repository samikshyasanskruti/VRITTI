
def generate_career_roadmap(
    resume_profile: dict,
    target_role: str,
    job_matches: list[dict] | None = None,
) -> dict:
    """Create a practical roadmap from detected skills and role requirements."""

    target_role = (target_role or "").strip()

    if not target_role:
        return {
            "success": False,
            "message": "Please provide a target job role.",
            "roadmap": [],
        }

    profile_skills = {
        str(skill).strip().lower()
        for skill in (resume_profile.get("skills") or [])
        if str(skill).strip()
    }

    required = set()
    preferred = set()

    for job in job_matches or []:
        job_title = str(job.get("title") or "").lower()

        if target_role.lower() not in job_title:
            continue

        required.update(
            str(skill).strip()
            for skill in (job.get("required_skills") or [])
            if str(skill).strip()
        )
        preferred.update(
            str(skill).strip()
            for skill in (job.get("preferred_skills") or [])
            if str(skill).strip()
        )

    missing_required = sorted(
        skill for skill in required
        if skill.lower() not in profile_skills
    )

    missing_preferred = sorted(
        skill for skill in preferred
        if skill.lower() not in profile_skills
    )

    roadmap = [
        {
            "phase": "Phase 1",
            "duration": "Week 1",
            "title": "Review your current skills",
            "tasks": [
                "Review the skills detected in your resume.",
                "Compare them with the target role's job descriptions.",
            ],
        },
        {
            "phase": "Phase 2",
            "duration": "Weeks 2-3",
            "title": "Address skill gaps",
            "tasks": [
                f"Study and practise: {skill}"
                for skill in missing_required
            ] or [
                "Choose a relevant technical topic and deepen your practical knowledge."
            ],
        },
        {
            "phase": "Phase 3",
            "duration": "Weeks 4-5",
            "title": "Build practical evidence",
            "tasks": [
                "Build a project relevant to your target role.",
                "Document your approach, implementation, and results.",
            ],
        },
        {
            "phase": "Phase 4",
            "duration": "Week 6",
            "title": "Prepare for applications",
            "tasks": [
                "Update your resume with verified project experience.",
                "Practise role-specific interview questions.",
                "Apply to relevant openings and review their requirements.",
            ],
        },
    ]

    return {
        "success": True,
        "target_role": target_role,
        "existing_skills": sorted(profile_skills),
        "missing_required_skills": missing_required,
        "missing_preferred_skills": missing_preferred,
        "roadmap": roadmap,
        "note": (
            "Roadmap duration is a suggested plan. Job-specific skill gaps "
            "can only be assessed when matching job records contain skills."
        ),
    }
