# ──────────────────────────────────────────────────────────────────────────────
# Stage 1: base — slim Python 3.12 image, no unnecessary OS packages
# ──────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

# Keeps Python from writing .pyc files to disk and from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

WORKDIR /app

# Create non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

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
        pytest-xdist \
        black \
        isort \
        ruff \
        bandit[toml] \
        mypy

# ──────────────────────────────────────────────────────────────────────────────
# Stage 3: lint — code quality and style checks
# ──────────────────────────────────────────────────────────────────────────────
FROM deps AS lint

# Copy source code for linting
COPY mars_rover/ ./mars_rover/
COPY tests/ ./tests/

# Run all linting and formatting checks
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

# Copy the application package and the test suite
COPY mars_rover/ ./mars_rover/
COPY tests/ ./tests/

# Ensure the non-root user can write pytest cache and coverage artifacts.
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Default command: run the full test suite with coverage and verbose output.
# Exit code propagates to Docker (non-zero = failed build / CI failure).
CMD ["pytest", "tests/", "-v", "--tb=short", "--cov=mars_rover", "--cov-report=term-missing", "--cov-report=html", "--cov-fail-under=90"]

# ──────────────────────────────────────────────────────────────────────────────
# Stage 5: runtime — minimal production image
# ──────────────────────────────────────────────────────────────────────────────
FROM base AS runtime

# Copy only the application code (no tests, no dev dependencies)
COPY mars_rover/ ./mars_rover/

# Switch to non-root user
USER appuser

# Set the module as executable
ENV PYTHONPATH=/app

# Default command: run the Mars Rover CLI
CMD ["python", "-m", "mars_rover"]
