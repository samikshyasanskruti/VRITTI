
from backend.app.services.embeddings.embedding_model import (
    DEFAULT_MODEL,
    encode_texts,
    get_embedding_model,
)
from backend.app.services.embeddings.job_embeddings import embed_jobs
from backend.app.services.embeddings.resume_embeddings import embed_resume
from backend.app.services.embeddings.similarity import (
    cosine_similarity,
    cosine_similarities,
)

__all__ = [
    "DEFAULT_MODEL",
    "encode_texts",
    "get_embedding_model",
    "embed_jobs",
    "embed_resume",
    "cosine_similarity",
    "cosine_similarities",
]
