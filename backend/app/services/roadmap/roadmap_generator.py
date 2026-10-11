
from backend.app.services.roadmap.learning_recommendations import (
    recommend_learning_resources,
)


def generate_roadmap(
    current_skills: list[str],
    target_role: str,
    missing_skills: list[str] | None = None,
) -> dict:
    """Build a staged learning roadmap based on supplied skill gaps."""

    target_role = (target_role or "").strip()
    if not target_role:
        raise ValueError("A target role is required.")

    existing = sorted({
        str(skill).strip()
        for skill in (current_skills or [])
        if str(skill).strip()
    })

    gaps = list(dict.fromkeys(
        str(skill).strip()
        for skill in (missing_skills or [])
        if str(skill).strip()
    ))

    resources = recommend_learning_resources(gaps)

    roadmap = [
        {
            "phase": 1,
            "title": "Review fundamentals",
            "duration": "Week 1",
            "tasks": [
                f"Review existing skills relevant to {target_role}.",
                "Identify knowledge gaps using actual job descriptions.",
            ],
        },
        {
            "phase": 2,
            "title": "Learn missing skills",
            "duration": "Weeks 2-3",
            "tasks": [
                f"Study {skill} and practise its core concepts."
                for skill in gaps[:5]
            ] or [
                "Choose a role-relevant topic to deepen your knowledge."
            ],
        },
        {
            "phase": 3,
            "title": "Build a practical project",
            "duration": "Weeks 4-5",
            "tasks": [
                f"Build a project demonstrating skills for {target_role}.",
                "Document the implementation and results.",
            ],
        },
        {
            "phase": 4,
            "title": "Prepare for applications",
            "duration": "Week 6",
            "tasks": [
                "Update your resume with verified skills and project evidence.",
                "Practise technical and behavioural interview questions.",
            ],
        },
    ]

    return {
        "target_role": target_role,
        "current_skills": existing,
        "missing_skills": gaps,
        "learning_resources": resources,
        "roadmap": roadmap,
        "note": "Durations are suggested planning estimates, not guarantees.",
    }
