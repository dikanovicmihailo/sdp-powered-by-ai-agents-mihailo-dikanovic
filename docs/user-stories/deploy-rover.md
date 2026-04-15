# STORY-002 — Deploy a Rover

## Story

> As an **operator**,
> I want to deploy a rover at a starting position and heading,
> so that it is ready to receive and execute commands.

---

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC-1 | Starting position `1 2 N` | Rover is created | `rover.x == 1`, `rover.y == 2`, `rover.heading == Heading.N` |
| AC-2 | Any valid heading (`N`, `E`, `S`, `W`) | Rover is created | Heading is stored correctly |
| AC-3 | Rover is created | State is inspected | Position and heading are readable |

---

## Architecture References

- **FR-2** — rover accepts initial position `(x, y)` and cardinal heading
- **DC-2** — valid headings: `N`, `E`, `S`, `W`
- Components: `domain/rover.py` → `Rover`, `domain/heading.py` → `Heading`

---

## Backend

### Domain model — `mars_rover/domain/heading.py`

```python
from enum import Enum


class Heading(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    def turn_left(self) -> "Heading":
        order = [Heading.N, Heading.W, Heading.S, Heading.E]
        return order[(order.index(self) + 1) % 4]

    def turn_right(self) -> "Heading":
        order = [Heading.N, Heading.E, Heading.S, Heading.W]
        return order[(order.index(self) + 1) % 4]

    def delta(self) -> tuple[int, int]:
        """Returns (dx, dy) for one forward step in this heading."""
        return {
            Heading.N: (0, 1),
            Heading.E: (1, 0),
            Heading.S: (0, -1),
            Heading.W: (-1, 0),
        }[self]
```

### Domain model — `mars_rover/domain/rover.py`

```python
from dataclasses import dataclass
from mars_rover.domain.heading import Heading


@dataclass
class Rover:
    """Mutable entity. Accumulates state as commands are applied."""

    x: int
    y: int
    heading: Heading

    def execute(self, command) -> None:
        command(self)
```

**Design notes:**
- `Rover` is intentionally mutable (models a physical vehicle moving through space — see `08-cross-cutting-concepts.md`)
- `execute` accepts any callable that takes a `Rover` — this is the Command pattern (ADR / `04-solution-strategy.md`)
- `Heading` is an immutable enum; rotation methods return new values, never mutate

### Unit tests — `tests/domain/test_rover.py`

```python
from mars_rover.domain.heading import Heading
from mars_rover.domain.rover import Rover


def test_rover_initial_state():
    rover = Rover(1, 2, Heading.N)
    assert rover.x == 1
    assert rover.y == 2
    assert rover.heading == Heading.N


def test_rover_all_headings():
    for heading in Heading:
        rover = Rover(0, 0, heading)
        assert rover.heading == heading
```

### Unit tests — `tests/domain/test_heading.py`

```python
from mars_rover.domain.heading import Heading


def test_turn_left_from_north():
    assert Heading.N.turn_left() == Heading.W


def test_turn_left_full_circle():
    h = Heading.N
    for _ in range(4):
        h = h.turn_left()
    assert h == Heading.N


def test_turn_right_from_north():
    assert Heading.N.turn_right() == Heading.E


def test_turn_right_full_circle():
    h = Heading.N
    for _ in range(4):
        h = h.turn_right()
    assert h == Heading.N


def test_delta_north():
    assert Heading.N.delta() == (0, 1)


def test_delta_east():
    assert Heading.E.delta() == (1, 0)


def test_delta_south():
    assert Heading.S.delta() == (0, -1)


def test_delta_west():
    assert Heading.W.delta() == (-1, 0)
```

---

## Frontend

No UI for this story. Rover deployment is expressed via the stdin text format:

```
1 2 N
```

Parsing is covered in STORY-007 (CLI input). Display of the deployed rover's final state is covered in STORY-004.

---

## Infrastructure

No infrastructure changes. Rover state is in-memory only for the duration of a single CLI run.

---

## Definition of Done

- [ ] `Heading` enum implemented in `mars_rover/domain/heading.py`
- [ ] `Rover` dataclass implemented in `mars_rover/domain/rover.py`
- [ ] All heading rotation and delta tests pass
- [ ] All rover initialisation tests pass
- [ ] `ruff`, `black`, and `isort` pass with no warnings
- [ ] No imports from `adapters/` or `application/` inside `domain/`
