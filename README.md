# CareerMatch AI — Backend package

This package keeps the supplied repository layout and uses the two supplied real datasets:
- `data/raw/resumes/Resume.zip` — source archive containing `Resume.csv` (ID, Resume_str, Resume_html, Category).
- `data/raw/internships/postings.csv.zip` — source archive containing `postings.csv` (job posting data).

No synthetic records are generated. The postings dataset contains job postings, not guaranteed internships; results are labeled as postings and should not be represented as verified active internship vacancies.

## Windows setup (PowerShell)

From the project root:
```powershell
py -3.10 -m venv backend\.venv
.\backend\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
$env:PYTHONPATH=(Get-Location).Path
python scripts\ingest_datasets.py
python scripts\build_faiss_index.py
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
Open `http://127.0.0.1:8000/docs`. Upload a real PDF/DOCX/TXT at `POST /api/resume/upload`. Frontend origins on localhost:5173 are allowed.

## APIs
- `GET /health`, `GET /api/health`
- `POST /api/resume/upload`, `GET /api/resume`, `GET /api/resume/{resume_id}`
- `GET /api/jobs`, `GET /api/jobs/{job_id}`, `POST /api/jobs`
- `POST /api/matching/run?resume_id=1&top_k=20`
- `GET /api/recommendations?resume_id=1`
- `POST /api/simulator/what-if`
- `POST /api/roadmap`
- `POST /api/recruiter/rank-candidates`

Scores are reproducible alignment scores, not probabilities of being hired. TF-IDF cosine similarity is the local baseline; it does not claim to use a pretrained transformer or FAISS. Extend with Sentence Transformers/FAISS when environment resources allow.


## Sentence Transformers + FAISS pipeline

The semantic engine uses `sentence-transformers/all-MiniLM-L6-v2` and normalized embeddings with FAISS `IndexFlatIP` (inner product equals cosine similarity for normalized vectors). The first model load downloads model weights and therefore needs internet access; later runs use the local model cache. The index is built from the real ingested postings and persisted under `vector_store/faiss/`.

Rebuild the index after adding/changing postings:
```powershell
python scripts/build_faiss_index.py
```

The current `/api/matching/run` computes semantic similarities directly using Sentence Transformers for all stored postings, then combines semantic similarity with required-skill coverage. The FAISS index is available for retrieval via `backend.app.services.retrieval.search.search_jobs`; use it to shortlist candidates when scaling to larger posting datasets. If the model cannot be downloaded, install/cache the model first rather than silently substituting fake embeddings.
