
from pathlib import Path
import argparse
import json
import logging

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "vector_store/jobs"
INDEX_PATH = OUTPUT_DIR / "jobs.faiss"
METADATA_PATH = OUTPUT_DIR / "jobs_metadata.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_resources():
    for path in (INDEX_PATH, METADATA_PATH):
        if not path.exists():
            raise FileNotFoundError(
                f"Required file not found: {path}. "
                "Run ingest_datasets.py, build_embeddings.py, "
                "and build_faiss_index.py first."
            )

    index = faiss.read_index(str(INDEX_PATH))

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    if index.ntotal != len(metadata):
        raise ValueError(
            "FAISS index and metadata counts do not match. "
            "Rebuild the embeddings and index."
        )

    model = SentenceTransformer(MODEL_NAME)
    return index, metadata, model


def match_jobs(resume_text, index, metadata, model, top_k=10):
    if not resume_text.strip():
        raise ValueError("Resume text is empty.")

    query_vector = model.encode(
        [resume_text],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    query_vector = np.asarray(query_vector, dtype=np.float32)

    top_k = max(1, min(top_k, index.ntotal))
    scores, indices = index.search(query_vector, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        job = metadata[int(idx)].copy()
        job["similarity_score"] = round(float(score), 4)
        results.append(job)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Find jobs semantically similar to a resume."
    )
    parser.add_argument(
        "--resume-file",
        required=True,
        help="Path to a plain-text resume file.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=10,
        help="Number of jobs to return (default: 10).",
    )
    args = parser.parse_args()

    resume_path = Path(args.resume_file)
    if not resume_path.is_absolute():
        resume_path = ROOT / resume_path

    if not resume_path.exists():
        raise FileNotFoundError(f"Resume file not found: {resume_path}")

    resume_text = resume_path.read_text(encoding="utf-8").strip()

    index, metadata, model = load_resources()
    results = match_jobs(
        resume_text,
        index,
        metadata,
        model,
        top_k=args.top_k,
    )

    if not results:
        print("No matching jobs were found.")
        return

    print("\nTop matching jobs\n" + "=" * 60)

    for rank, job in enumerate(results, start=1):
        print(f"\n{rank}. {job['title'] or 'Untitled position'}")
        print(f"   Company: {job['company'] or 'Not specified'}")
        print(f"   Location: {job['location'] or 'Not specified'}")
        print(f"   Similarity: {job['similarity_score']:.4f}")

        if job["source_url"]:
            print(f"   URL: {job['source_url']}")


if __name__ == "__main__":
    main()
