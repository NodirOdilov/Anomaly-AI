# syntax=docker/dockerfile:1.7
# === Builder stage: компилируем wheels, чтобы runtime не тащил build-tools ===
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Системные зависимости для argon2/cryptography/asyncpg.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --wheel-dir=/wheels -r requirements.txt


# === Runtime stage: чистый минимальный образ ===
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PIP_NO_CACHE_DIR=1

# Runtime библиотеки (без build-essential).
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 anomaly

WORKDIR /app

# Установка из заранее собранных wheels.
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

# Копируем исходный код. В production маунт data/models — через volume.
COPY --chown=anomaly:anomaly pyproject.toml pytest.ini alembic.ini ./
COPY --chown=anomaly:anomaly configs ./configs
COPY --chown=anomaly:anomaly data ./data
COPY --chown=anomaly:anomaly reports ./reports
COPY --chown=anomaly:anomaly migrations ./migrations
COPY --chown=anomaly:anomaly src ./src

USER anomaly

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["uvicorn", "anomaly_ai.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
