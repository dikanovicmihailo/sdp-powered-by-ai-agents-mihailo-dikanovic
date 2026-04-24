# 02. Architecture Constraints

## Technical Constraints

| ID   | Constraint | Rationale |
|------|-----------|-----------|
| TC-1 | Implemented in **Python ≥ 3.12** | Course toolchain defined in `pyproject.toml` |
| TC-2 | No external runtime dependencies for core domain logic | Keeps the domain pure, portable, and fast to test |
| TC-3 | Input/output via **stdin / stdout** (CLI) | Simplest integration surface; trivially scriptable and testable |
| TC-4 | Code style enforced by **black**, **isort**, and **ruff** | Configured in `pyproject.toml`; enforced via pre-commit hooks |

## Organisational Constraints

| ID   | Constraint | Rationale |
|------|-----------|-----------|
| OC-1 | Architecture documented using the **arc42** template | Course requirement for Module 2 |
| OC-2 | C4 diagrams authored in **PlantUML** | Pre-commit hook (`validate-plantuml.sh`) already validates `.puml` files |
| OC-3 | Commit messages follow a defined convention | Enforced by `check-commit-msg.sh` pre-commit hook |

## Domain Constraints

| ID   | Constraint |
|------|-----------|
| DC-1 | The plateau is a finite rectangular grid; the lower-left corner is always `(0, 0)` |
| DC-2 | Valid headings: `N`, `E`, `S`, `W` (cardinal directions only) |
| DC-3 | Valid commands: `L` (turn left 90°), `R` (turn right 90°), `M` (move one step forward) |
| DC-4 | Rovers are processed sequentially — no concurrent movement |
| DC-5 | A rover that would move outside the plateau **stays in place** (safe-stop); no error is raised |
| DC-6 | *(Optional)* If obstacles are present, a rover stops before the obstacle and reports its last safe position |
