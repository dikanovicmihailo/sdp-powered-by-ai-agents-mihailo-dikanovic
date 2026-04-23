# ──────────────────────────────────────────────────────────────────────────────
# Stage 1: base — slim Python 3.12 image, no unnecessary OS packages
# ──────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# ──────────────────────────────────────────────────────────────────────────────
# Stage 2: deps — install only test / dev dependencies (no .venv, no root)
# ──────────────────────────────────────────────────────────────────────────────
FROM base AS deps

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ──────────────────────────────────────────────────────────────────────────────
# Stage 3: lint — code quality and style checks
# ──────────────────────────────────────────────────────────────────────────────
FROM deps AS lint

COPY pyproject.toml .
COPY mars_rover/ ./mars_rover/
COPY tests/ ./tests/

RUN echo "Running code quality checks..." && \
    black --check --diff mars_rover/ tests/ && \
    echo "✓ Black formatting check passed" && \
    isort --check-only --diff mars_rover/ tests/ && \
    echo "✓ Import sorting check passed" && \
    ruff check mars_rover/ tests/ && \
    echo "✓ Ruff linting passed" && \
    bandit -r mars_rover/ -f json -o bandit-report.json && \
    echo "✓ Security scan completed"

# ──────────────────────────────────────────────────────────────────────────────
# Stage 4: test — copy source + tests and run the suite
# ──────────────────────────────────────────────────────────────────────────────
FROM deps AS test

COPY pyproject.toml .
COPY mars_rover/ ./mars_rover/
COPY tests/ ./tests/

RUN chown -R appuser:appuser /app

USER appuser

CMD ["pytest", "tests/", "-v", "--tb=short", "--cov=mars_rover", "--cov-report=term-missing", "--cov-report=html:/tmp/htmlcov", "--cov-fail-under=90"]
# ──────────────────────────────────────────────────────────────────────────────
# Stage 5: runtime — minimal production image
# ──────────────────────────────────────────────────────────────────────────────
FROM base AS runtime

COPY pyproject.toml .
COPY mars_rover/ ./mars_rover/

USER appuser

ENV PYTHONPATH=/app

CMD ["python", "-m", "mars_rover"]
