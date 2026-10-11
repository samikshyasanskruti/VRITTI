from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv("CAREERMATCH_DATA_DIR", PROJECT_ROOT / "data")).resolve()
RAW_RESUMES_DIR = DATA_DIR / "raw" / "resumes"
RAW_INTERNSHIPS_DIR = DATA_DIR / "raw" / "internships"
RAW_JOBS_DIR = DATA_DIR / "raw" / "job_descriptions"
PROCESSED_DIR = DATA_DIR / "processed"
DATABASE_PATH = Path(os.getenv("CAREERMATCH_DATABASE_PATH", DATA_DIR / "database" / "careermatch.db"))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH.as_posix()}")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "15"))
ALLOWED_ORIGINS = [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()]
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "tfidf")
