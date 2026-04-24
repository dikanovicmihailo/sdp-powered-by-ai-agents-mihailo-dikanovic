# 08. Cross-Cutting Concepts

Cross-cutting concepts are design decisions and patterns that apply across multiple building blocks rather than belonging to a single component.

---

## Domain Model

The domain is modelled as a set of **pure value objects and entities** with no dependencies on I/O, frameworks, or infrastructure. This is enforced by the hexagonal architecture: the `domain/` package must never import from `adapters/` or `application/`.

---

## Error Handling

| Situation | Behaviour |
|-----------|-----------|
| Rover would move outside the plateau | Silent safe-stop — position unchanged, processing continues |
| Rover would move into an obstacle *(optional)* | Silent safe-stop — position unchanged, mission for that rover ends |
| Malformed input (bad heading, unknown command) | `ValueError` raised in `InputParser`; propagates to `__main__` which prints an error message to stderr and exits with code 1 |

Errors in the domain are **never swallowed silently** — only the two safe-stop cases above are intentional no-ops.

---

## Immutability and State

- `Plateau` is **immutable** after construction — its dimensions never change during a mission.
- `Heading` is an **immutable enum** — rotation methods return a new `Heading` value.
- `Rover` is **mutable** — it accumulates state changes as commands are applied. This is intentional; it models the physical rover moving through space.

---

## Testability

All domain classes are designed to be instantiated directly in tests with no mocking required:

```python
plateau = Plateau(5, 5)
rover = Rover(1, 2, Heading.N)
rover.execute(MoveForward(plateau))
assert rover.x == 1
assert rover.y == 3
```

The `InputParser` and `OutputFormatter` are tested with plain strings — no file handles or subprocess calls needed.

---

## Logging

The system is a simple CLI kata — no structured logging framework is used. Debug output, if needed, goes to `stderr` so it does not pollute the `stdout` result stream.

---

## Input / Output Format

The text protocol is intentionally minimal:

```
# Plateau (upper-right corner; lower-left is always 0 0)
5 5

# Per rover: initial position line, then command string line
1 2 N
LMLMLMLMM
```

Parsing is centralised in `InputParser`. No other component reads raw strings.

---

## Code Style

Enforced uniformly across the entire codebase via pre-commit hooks:

| Tool | Purpose |
|------|---------|
| `black` | Opinionated code formatting |
| `isort` | Import ordering |
| `ruff` | Fast linting (style, complexity, unused imports) |
