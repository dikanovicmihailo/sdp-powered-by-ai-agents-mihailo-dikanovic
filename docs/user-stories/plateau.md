# STORY-001 — Define the Plateau

## Story

> As an **operator**,
> I want to define a rectangular plateau by its upper-right corner coordinates,
> so that rovers have a bounded grid to navigate within.

---

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC-1 | Upper-right corner `5 5` | Plateau is created | Grid spans `(0,0)` to `(5,5)` inclusive |
| AC-2 | Any point `(x, y)` with `0 ≤ x ≤ width` and `0 ≤ y ≤ height` | `is_within(x, y)` is called | Returns `True` |
| AC-3 | Any point outside those bounds (e.g. `(6, 0)`, `(-1, 3)`) | `is_within(x, y)` is called | Returns `False` |
| AC-4 | Plateau is created | Any subsequent operation | Dimensions never change (immutable after construction) |

---

## Architecture References

- **FR-1** — plateau defined by upper-right corner; lower-left is always `(0, 0)`
- **DC-1** — finite rectangular grid constraint
- **QS-3 / QS-4** — boundary safety scenarios depend on this component
- Component: `domain/plateau.py` → `Plateau`

---

## Backend

### Domain model — `mars_rover/domain/plateau.py`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Plateau:
    """Immutable rectangular grid. Lower-left is always (0, 0)."""

    width: int
    height: int

    def is_within(self, x: int, y: int) -> bool:
        return 0 <= x <= self.width and 0 <= y <= self.height
```

**Design notes:**
- `frozen=True` enforces immutability (AC-4, cross-cutting concept from `08-cross-cutting-concepts.md`)
- No I/O, no framework imports — pure domain object (TC-2)
- `is_within` is the single boundary-check entry point used by `MoveForward` (see STORY-005)

### Unit tests — `tests/domain/test_plateau.py`

```python
import pytest
from mars_rover.domain.plateau import Plateau


def test_plateau_contains_origin():
    assert Plateau(5, 5).is_within(0, 0) is True


def test_plateau_contains_upper_right_corner():
    assert Plateau(5, 5).is_within(5, 5) is True


def test_plateau_contains_interior_point():
    assert Plateau(5, 5).is_within(3, 2) is True


def test_plateau_rejects_x_too_large():
    assert Plateau(5, 5).is_within(6, 0) is False


def test_plateau_rejects_y_too_large():
    assert Plateau(5, 5).is_within(0, 6) is False


def test_plateau_rejects_negative_x():
    assert Plateau(5, 5).is_within(-1, 3) is False


def test_plateau_rejects_negative_y():
    assert Plateau(5, 5).is_within(3, -1) is False


def test_plateau_is_immutable():
    plateau = Plateau(5, 5)
    with pytest.raises(Exception):
        plateau.width = 10  # type: ignore[misc]
```

---

## Frontend

No UI for this story. The plateau is defined via stdin text (see STORY-007 — CLI pipe input).

The output contract for the operator is covered in STORY-004.

---

## Infrastructure

No infrastructure changes required. The plateau lives entirely in memory for the duration of a single CLI invocation (see `07-deployment.md` — single-process CLI, no persistence).

---

## Definition of Done

- [ ] `Plateau` dataclass implemented in `mars_rover/domain/plateau.py`
- [ ] All 8 unit tests pass (`pytest tests/domain/test_plateau.py`)
- [ ] `ruff`, `black`, and `isort` pass with no warnings
- [ ] No imports from `adapters/` or `application/` inside `domain/`
