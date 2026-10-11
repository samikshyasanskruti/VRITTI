
import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_model_cache = {}


def get_embedding_model(model_name: str = DEFAULT_MODEL):
    """Load and cache an embedding model."""
    if model_name not in _model_cache:
        _model_cache[model_name] = SentenceTransformer(model_name)
    return _model_cache[model_name]


def encode_texts(
    texts: list[str],
    model_name: str = DEFAULT_MODEL,
) -> np.ndarray:
    """Encode texts into normalized float32 embeddings."""
    if not texts:
        return np.empty((0, 384), dtype=np.float32)

    model = get_embedding_model(model_name)

    vectors = model.encode(
        [str(text or "") for text in texts],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return np.asarray(vectors, dtype=np.float32)
