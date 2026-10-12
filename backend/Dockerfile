
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY backend/requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir --retries 10 --timeout 180 --index-url https://pypi.org/simple -r requirements.txt
COPY backend/app ./backend/app

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
