# 04. Solution Strategy

## Architectural Style — Hexagonal (Ports & Adapters)

The domain logic is completely isolated from I/O. The CLI is just one possible adapter; the same domain could be driven by an HTTP API or a test suite without any changes to the core.

```
┌─────────────────────────────────────────────────────┐
│                  CLI Adapter (stdin/stdout)          │
│   InputParser                    OutputFormatter     │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              Application Layer                       │
│              MissionController                       │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                  Domain Layer                        │
│   Plateau   Rover   Heading   Command (protocol)     │
└─────────────────────────────────────────────────────┘
```

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Domain isolation | Hexagonal architecture | Domain has zero I/O dependencies; fully unit-testable |
| Command processing | **Command pattern** — each instruction is a callable that transforms `Rover` state | Adding new commands requires no changes to existing code (open/closed principle) |
| Heading rotation | `Heading` enum owns `turn_left()` / `turn_right()` | Rotation logic lives in one place; no conditionals scattered across the codebase |
| Boundary enforcement | `Plateau.is_within(x, y)` called inside `MoveForward` | Domain rule stays in the domain; adapter never needs to know about grid limits |
| Input parsing | Dedicated `InputParser` in the adapter layer | Keeps raw string handling out of the domain |

## Technology Choices

| Concern | Choice |
|---------|--------|
| Language | Python 3.12 |
| Testing | `pytest` |
| Linting / formatting | `ruff`, `black`, `isort` |
| Diagram format | PlantUML (C4 model) |
