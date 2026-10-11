
import numpy as np


def cosine_similarity(vector_a, vector_b) -> float:
    """Calculate cosine similarity between two vectors."""
    a = np.asarray(vector_a, dtype=np.float32).reshape(-1)
    b = np.asarray(vector_b, dtype=np.float32).reshape(-1)

    if a.shape != b.shape:
        raise ValueError("Embedding vectors must have the same dimensions.")

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def cosine_similarities(query_vector, matrix) -> np.ndarray:
    """Calculate cosine similarities against a matrix of vectors."""
    query = np.asarray(query_vector, dtype=np.float32).reshape(-1)
    vectors = np.asarray(matrix, dtype=np.float32)

    if vectors.ndim != 2 or vectors.shape[1] != query.shape[0]:
        raise ValueError("Query and embedding matrix dimensions do not match.")

    query_norm = np.linalg.norm(query)
    vector_norms = np.linalg.norm(vectors, axis=1)
    denominators = vector_norms * query_norm

    return np.divide(
        vectors @ query,
        denominators,
        out=np.zeros(len(vectors), dtype=np.float32),
        where=denominators > 0,
    )
