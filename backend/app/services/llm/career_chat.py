
import os
from typing import Any

import requests


def career_chat(
    message: str,
    resume_profile: dict | None = None,
    job_matches: list[dict] | None = None,
) -> dict[str, Any]:
    """
    Answer career-related questions using available resume and job context.
    Uses Ollama when available; otherwise returns a transparent fallback.
    """
    message = (message or "").strip()

    if not message:
        return {
            "success": False,
            "answer": "Please enter a career-related question.",
            "provider": "none",
        }

    resume_profile = resume_profile or {}
    job_matches = job_matches or []

    context = (
        "Resume profile:\n"
        f"{resume_profile}\n\n"
        "Available job matches:\n"
        f"{job_matches[:5]}\n\n"
        "Answer using the supplied context. Do not invent resume details, "
        "job openings, qualifications, or hiring outcomes."
    )

    prompt = f"{context}\n\nCandidate question: {message}"

    ollama_url = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434/api/generate",
    )
    model = os.getenv("OLLAMA_MODEL", "llama3.2")

    try:
        response = requests.post(
            ollama_url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        answer = (data.get("response") or "").strip()

        if answer:
            return {
                "success": True,
                "answer": answer,
                "provider": "ollama",
                "model": model,
            }

    except requests.RequestException:
        pass

    return {
        "success": True,
        "answer": (
            "I could not connect to the local AI model. "
            "Please check that Ollama is running and the configured model "
            f"'{model}' is installed. Your question was: {message}"
        ),
        "provider": "fallback",
    }
