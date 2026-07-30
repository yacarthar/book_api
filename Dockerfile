# syntax=docker/dockerfile:1.7
FROM python:3.11-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
  pip install -r requirements.txt

# ---------- test image ----------

FROM base AS test

COPY . .


# ---------- runtime image ----------

FROM base AS runtime

COPY app ./app
COPY migrations ./migrations
COPY alembic.ini .
COPY config.py .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]