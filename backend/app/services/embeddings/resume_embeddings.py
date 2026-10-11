
from backend.app.services.embeddings.embedding_model import (
    encode_texts,
    DEFAULT_MODEL,
)


def embed_resume(
    resume_text: str,
    model_name: str = DEFAULT_MODEL,
):
    """Generate one embedding vector for a resume."""
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    return encode_texts(
        [resume_text],
        model_name=model_name,
    )[0]
