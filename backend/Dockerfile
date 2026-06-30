# Forja — backend (FastAPI + LangGraph + Playwright)
# Contexto de build: ./backend
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# git é necessário para o nó deploy (branch/commit/push).
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Dependências Python + navegador do Playwright (Chromium) com libs de SO.
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && python -m playwright install --with-deps chromium

COPY . /app

# REPO_ROOT é montado em runtime (volume) — o repo dos objetos educacionais.
ENV REPO_ROOT=/repo \
    FORJA_DB=/app/forja.db

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
