
from backend.app.services.embeddings.embedding_model import (
    encode_texts,
    DEFAULT_MODEL,
)


def embed_jobs(
    jobs: list[dict],
    model_name: str = DEFAULT_MODEL,
):
    """Generate embeddings from job titles and descriptions."""
    texts = [
        f"{job.get('title') or ''}\n{job.get('description') or ''}"
        for job in jobs
    ]

    return encode_texts(texts, model_name=model_name)
