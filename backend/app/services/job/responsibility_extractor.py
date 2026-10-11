
import re
import sqlite3


SECTION_HEADINGS = [
    "Agent Assistance",
    "Graphic Design & Branding",
    "Events & Community",
]

TASK_STARTS = [
    "Organize",
    "Communicate",
    "Prepare",
    "Submit",
    "Track",
    "Manage",
    "Managing",
    "Prioritize",
    "Fulfill",
    "Maintain",
    "Plan",
    "Execute",
    "Receive",
]

ACTION_PATTERN = re.compile(
    r"\b(?:organize|communicate|prepare|submit|track|manage|managing|"
    r"prioritize|fulfill|maintain|plan|execute|receive|design|create|"
    r"develop|coordinate|support|update|monitor|assist)\b",
    re.IGNORECASE,
)

INCOMPLETE_ENDING = re.compile(
    r"(?:&|and|or|to|for|with|using|including|pre|of|in|on|by)$",
    re.IGNORECASE,
)

STOP_PATTERN = re.compile(
    r"(?i)\b(?:our company is committed|equal opportunity employer|"
    r"what experience do i need|what benefits do i receive|"
    r"job type\s*:|expected hours\s*:|work location\s*:|"
    r"benefits\s*:)"
)


def extract_responsibilities(description: str) -> list[str]:
    if not description:
        return []

    text = re.sub(r"\s+", " ", description).strip()

    # Repair a known missing separator in the source dataset.
    text = re.sub(
        r"(?i)(sponsorships)\s*(our company is committed)",
        r"\1. \2",
        text,
    )

    # Remove employment metadata and employer-policy text.
    stop = STOP_PATTERN.search(text)
    if stop:
        text = text[:stop.start()].strip()

    # Find the first known responsibilities heading.
    headings = "|".join(map(re.escape, SECTION_HEADINGS))
    heading = re.search(
        rf"(?i)(?:{headings})\s*[-–—:]",
        text,
    )

    if not heading:
        return []

    text = text[heading.start():]

    # Separate inline headings and dash-delimited tasks.
    text = re.sub(
        rf"(?i)(?=(?:{headings})\s*[-–—:])",
        "\n",
        text,
    )
    text = re.sub(r"\s*[-–—]\s*", "\n", text)

    # Split common concatenated task transitions.
    task_pattern = (
        r"(?i)(?<!^)(?=("
        + "|".join(map(re.escape, TASK_STARTS))
        + r")\b)"
    )
    text = re.sub(task_pattern, "\n", text)

    results = []

    for line in text.splitlines():
        line = line.strip(" \t-–—:,.")
        if not line:
            continue

        # Remove section labels.
        for section in SECTION_HEADINGS:
            line = re.sub(
                r"(?i)^" + re.escape(section) + r"\s*",
                "",
                line,
            )

        line = re.sub(r"\s+", " ", line).strip(" \t-–—:,. ")

        if len(line) < 25 or len(line.split()) < 5:
            continue

        if STOP_PATTERN.search(line):
            continue

        if INCOMPLETE_ENDING.search(line.rstrip(" .")):
            continue

        if ACTION_PATTERN.search(line):
            results.append(line.rstrip(" ."))

    return list(dict.fromkeys(results))


if __name__ == "__main__":
    with sqlite3.connect("data/database/dataset.db") as conn:
        row = conn.execute(
            "SELECT title, description FROM dataset_jobs LIMIT 1"
        ).fetchone()

    if row:
        responsibilities = extract_responsibilities(row[1] or "")

        print("Job:", row[0])
        print("Responsibilities found:", len(responsibilities))

        for item in responsibilities:
            print("-", item)
