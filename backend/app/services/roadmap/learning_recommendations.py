
def recommend_learning_resources(
    missing_skills: list[str],
    top_k: int = 10,
) -> list[dict]:
    """Suggest learning topics for skills missing from a resume."""

    resources = {
        "python": {
            "type": "Official tutorial",
            "url": "https://docs.python.org/3/tutorial/",
        },
        "sql": {
            "type": "Interactive learning",
            "url": "https://sqlbolt.com/",
        },
        "machine learning": {
            "type": "Course",
            "url": "https://www.coursera.org/learn/machine-learning",
        },
        "pandas": {
            "type": "Documentation",
            "url": "https://pandas.pydata.org/docs/",
        },
        "scikit-learn": {
            "type": "Documentation",
            "url": "https://scikit-learn.org/stable/user_guide.html",
        },
        "tensorflow": {
            "type": "Tutorials",
            "url": "https://www.tensorflow.org/tutorials",
        },
        "pytorch": {
            "type": "Tutorials",
            "url": "https://pytorch.org/tutorials/",
        },
        "docker": {
            "type": "Getting started",
            "url": "https://docs.docker.com/get-started/",
        },
        "fastapi": {
            "type": "Official tutorial",
            "url": "https://fastapi.tiangolo.com/tutorial/",
        },
        "git": {
            "type": "Book",
            "url": "https://git-scm.com/book/en/v2",
        },
    }

    results = []

    for skill in missing_skills or []:
        name = str(skill).strip()
        if not name:
            continue

        resource = resources.get(
            name.lower(),
            {
                "type": "Learning resource search",
                "url": (
                    "https://www.google.com/search?q="
                    + name.replace(" ", "+")
                    + "+official+tutorial"
                ),
            },
        )

        results.append({
            "skill": name,
            **resource,
        })

        if len(results) >= max(1, top_k):
            break

    return results
