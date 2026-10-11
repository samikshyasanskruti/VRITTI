
def build_learning_path(
    prioritized_gaps: list[dict],
) -> list[dict]:
    """Turn prioritized skill gaps into an ordered learning plan."""

    tasks = []

    for index, item in enumerate(prioritized_gaps or [], start=1):
        skill = item.get("skill", "Unspecified skill")
        priority = item.get("priority", "Unclassified")

        tasks.append({
            "step": index,
            "skill": skill,
            "priority": priority,
            "suggested_activity": (
                f"Study the fundamentals of {skill}, complete practical "
                "exercises, and build a small project demonstrating it."
            ),
        })

    return tasks
