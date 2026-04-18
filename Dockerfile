# ──────────────────────────────────────────────────────────────────────────────
# Stage 1: base — slim Python 3.12 image, no unnecessary OS packages
# ──────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

# Keeps Python from writing .pyc files to disk and from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ──────────────────────────────────────────────────────────────────────────────
# Stage 2: deps — install only test / dev dependencies (no .venv, no root)
# ──────────────────────────────────────────────────────────────────────────────
FROM base AS deps

# Copy the project manifest first to leverage Docker layer caching:
# dependencies are only reinstalled when pyproject.toml changes.
COPY pyproject.toml .

# Install pytest and the linting/security tools referenced in pyproject.toml.
# The core domain has zero runtime dependencies (TC-2), so this is the complete
# dependency set needed to run the test suite.
RUN pip install --no-cache-dir \
        pytest \
        pytest-cov \
        black \
        isort \
        ruff \
        bandit[toml]

# ──────────────────────────────────────────────────────────────────────────────
# Stage 3: test — copy source + tests and run the suite
# ──────────────────────────────────────────────────────────────────────────────
FROM deps AS test

# Copy the application package and the test suite
COPY mars_rover/ ./mars_rover/
COPY tests/ ./tests/

# Default command: run the full test suite with verbose output.
# Exit code propagates to Docker (non-zero = failed build / CI failure).
CMD ["pytest", "tests/", "-v", "--tb=short"]
