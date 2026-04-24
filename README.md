# Mars Rover Kata

A Python implementation of the classic Mars Rover kata, built as part of the *Software Development Processes Powered by AI Agents* course. The kata demonstrates clean architecture, domain-driven design, and test-driven development — with every feature driven by AI agents for git workflow, architecture, requirements, CI/CD, and TDD/BDD.

---

## What the Kata Solves

A rover is deployed onto a rectangular plateau on Mars. An operator sends it a sequence of commands — turn left (`L`), turn right (`R`), or move forward (`M`). The system must:

- Accept a plateau size and one or more rovers with initial positions and headings
- Process each rover's command string sequentially
- Report the final position and heading of every rover
- Prevent any rover from leaving the plateau boundaries
- Detect obstacles and stop safely before collision

---

## Tech Stack & Architecture

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| CLI | `python -m mars_rover` (stdin pipe) |
| Testing | pytest + coverage |
| Linting | Black, isort, Ruff, Bandit |
| Docs | Sphinx + MyST + Wagtail theme → GitHub Pages |
| CI/CD | GitHub Actions |
| Containerisation | Docker (multi-stage) |

The codebase follows a **Ports & Adapters (Hexagonal)** architecture with three layers:

```
mars_rover/
├── domain/          # Pure business logic — Rover, Plateau, Heading, Commands
├── application/     # Use-case orchestration — MissionController
└── adapters/        # I/O translation — InputParser, OutputFormatter
```

The domain layer has zero I/O dependencies and is fully unit-testable in isolation.

---

## Build & Run Locally

**Run the application:**

```bash
# Build the runtime image
docker build --target runtime -t mars-rover .

# Run with piped input
echo -e "5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM" | docker run --rm -i mars-rover
```

**Expected output:**
```
1 3 N
5 1 E
```

---

## Run Tests

```bash
# Build the test image and run the full suite (lint + tests + coverage)
docker build --target test -t mars-rover-test .
docker run --rm mars-rover-test
```

The test stage runs pytest with `--cov-fail-under=90`. The lint stage (Black, isort, Ruff, Bandit) runs as a separate build target:

```bash
docker build --target lint -t mars-rover-lint .
```

---

## Documentation

Live Sphinx documentation is published to GitHub Pages on every push to `main`:

**[https://dikanovicmihailo.github.io/sdp-powered-by-ai-agents-mihailo-dikanovic/](https://dikanovicmihailo.github.io/sdp-powered-by-ai-agents-mihailo-dikanovic/)**

Docs source lives in `docs/` and covers architecture (arc42), user stories, and the glossary.

---

## Project Structure

```
.
├── mars_rover/
│   ├── domain/          # Rover, Plateau, Heading, Commands
│   ├── application/     # MissionController
│   ├── adapters/        # InputParser, OutputFormatter
│   └── __main__.py      # CLI entry point
├── tests/
│   ├── domain/          # Unit tests for domain logic
│   ├── application/     # Unit tests for use cases
│   ├── adapters/        # Unit tests for I/O adapters
│   └── test_cli_*.py    # End-to-end CLI tests
├── docs/
│   ├── architecture/    # arc42 documentation (12 sections)
│   └── user-stories/    # BDD user stories per feature
├── .github/workflows/   # CI pipeline + Sphinx deploy
├── Dockerfile           # Multi-stage: base → deps → lint → test → runtime
└── pyproject.toml       # Project metadata and tool config
```

---

## Author

**Mihailo Dikanovic**
GitHub: [@dikanovicmihailo](https://github.com/dikanovicmihailo)
