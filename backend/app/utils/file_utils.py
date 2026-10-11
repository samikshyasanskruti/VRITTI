from pathlib import Path
def safe_filename(filename): return Path(filename or 'upload').name
