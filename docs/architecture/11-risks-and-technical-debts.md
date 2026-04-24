# 11. Risks and Technical Debts

## Risks

| ID   | Risk | Probability | Impact | Mitigation |
|------|------|-------------|--------|------------|
| R-1 | **Silent boundary violations** — a rover silently stays in place when hitting a boundary; a misconfigured plateau could produce wrong results with no visible error | Low | Medium | Add an optional `--strict` flag that raises an error on boundary violation; log a warning to stderr |
| R-2 | **Input format ambiguity** — the kata does not define behaviour for malformed input (e.g. unknown command character, negative coordinates) | Medium | Low | `InputParser` raises `ValueError` with a descriptive message; covered by unit tests |
| R-3 | **Sequential processing assumption** — rovers are processed one at a time; if the kata is extended to simultaneous movement, the current design does not support collision detection between rovers | Low | High | Document the assumption explicitly (DC-4 in constraints); revisit `MissionController` if simultaneous movement is required |
| R-4 | **No persistence** — rover state exists only in memory during a single run; a crash loses all progress | Low | Low | Acceptable for a kata; a production system would need checkpointing |

---

## Technical Debts

| ID   | Debt | Impact | Remediation |
|------|------|--------|-------------|
| TD-1 | **No obstacle support in core domain** — `Plateau.is_within()` only checks boundaries; obstacle detection is not yet implemented | Low (optional feature) | Add `obstacles: set[tuple[int, int]]` to `Plateau`; extend `MoveForward` to call `is_blocked()` |
| TD-2 | **`Rover` is mutable** — command execution mutates rover state in place; this makes it harder to replay or undo a command sequence | Low | Introduce an immutable `RoverState` value object and make `Rover` a thin wrapper that produces new states |
| TD-3 | **No structured logging** — errors go to stderr as plain strings | Low | Acceptable for a kata; replace with `logging` module if the system grows |
| TD-4 | **Input format is positional / fragile** — the parser relies on line order and space-separated tokens; any deviation causes a crash | Medium | Add schema validation or a more robust parser with clear error messages per field |
