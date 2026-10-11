
import numpy as np

from backend.app.services.embeddings.embedding_model import (
    encode_texts,
    DEFAULT_MODEL,
)


def semantic_scores(
    resume_text: str,
    job_documents: list[str],
) -> list[float]:
    """Calculate cosine similarity between a resume and job descriptions."""
    if not job_documents:
        return []

    if not resume_text or not resume_text.strip():
        return [0.0] * len(job_documents)

    documents = [
        str(document or "").strip() or " "
        for document in job_documents
    ]

    embeddings = encode_texts(
        [resume_text] + documents,
        model_name=DEFAULT_MODEL,
    )

    embeddings = np.asarray(embeddings, dtype=np.float32)

    if embeddings.ndim != 2 or len(embeddings) != len(documents) + 1:
        raise ValueError("Unexpected embedding shape returned by encoder.")

    resume_vector = embeddings[0]
    job_vectors = embeddings[1:]

    resume_norm = np.linalg.norm(resume_vector)
    job_norms = np.linalg.norm(job_vectors, axis=1)

    denominator = job_norms * resume_norm
    similarities = np.divide(
        job_vectors @ resume_vector,
        denominator,
        out=np.zeros(len(documents), dtype=np.float32),
        where=denominator > 0,
    )

    return [
        float(np.clip(score, -1.0, 1.0))
        for score in similarities
    ]
