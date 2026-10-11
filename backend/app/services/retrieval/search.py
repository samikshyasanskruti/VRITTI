
from backend.app.services.embeddings.embedding_model import (
    encode_texts,
    DEFAULT_MODEL,
)
from backend.app.services.retrieval.index_loader import load_job_index
from backend.app.services.retrieval.faiss_engine import search_index


def search_jobs(query_text: str, top_k: int = 20) -> list[dict]:
    """Retrieve jobs using the existing FAISS index."""
    if not query_text or not query_text.strip():
        return []

    index, metadata = load_job_index()

    vectors = encode_texts(
        [query_text],
        model_name=metadata.get("model_name", DEFAULT_MODEL),
    )

    hits = search_index(index, vectors[0], top_k)

    results = []

    for idx, score in hits:
        record = metadata["records"][idx]

        results.append({
            **record,
            "semantic_similarity": round(max(0.0, score), 6),
        })

    return results
