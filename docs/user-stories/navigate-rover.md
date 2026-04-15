# STORY-003 — Navigate a Rover

## Story

> As an **operator**,
> I want to send a command string of `L`, `R`, and `M` instructions to a rover,
> so that it navigates the plateau and reaches its intended destination.

---

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC-1 | Rover at `(1, 2, N)` | Command `L` is executed | Rover is at `(1, 2, W)` |
| AC-2 | Rover at `(1, 2, N)` | Command `R` is executed | Rover is at `(1, 2, E)` |
| AC-3 | Rover at `(1, 2, N)` on plateau `5 5` | Command `M` is executed | Rover is at `(1, 3, N)` |
| AC-4 | Rover at `(1, 2, N)` on plateau `5 5` | Command string `LMLMLMLMM` | Rover ends at `(1, 3, N)` (kata example 1) |
| AC-5 | Rover at `(3, 3, E)` on plateau `5 5` | Command string `MMRMMRMRRM` | Rover ends at `(5, 1, E)` (kata example 2) |

---

## Architecture References

- **FR-3** — command string composed of `L`, `R`, `M`
- **QS-1 / QS-2** — correctness scenarios from `10-quality-requirements.md`
- **DC-3** — valid commands constraint
- Components: `domain/commands.py` → `TurnLeft`, `TurnRight`, `MoveForward`
- Pattern: Command pattern — each instruction is a callable that transforms `Rover` state

---

## Backend

### Domain model — `mars_rover/domain/commands.py`

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mars_rover.domain.rover import Rover
    from mars_rover.domain.plateau import Plateau


class TurnLeft:
    def __call__(self, rover: "Rover") -> None:
        rover.heading = rover.heading.turn_left()


class TurnRight:
    def __call__(self, rover: "Rover") -> None:
        rover.heading = rover.heading.turn_right()


class MoveForward:
    def __init__(self, plateau: "Plateau") -> None:
        self._plateau = plateau

    def __call__(self, rover: "Rover") -> None:
        dx, dy = rover.heading.delta()
        new_x, new_y = rover.x + dx, rover.y + dy
        if self._plateau.is_within(new_x, new_y):
            rover.x = new_x
            rover.y = new_y
        # else: safe-stop — position unchanged (see STORY-005)
```

**Design notes:**
- Each command is a callable class — adding a new command (e.g. `UTurn`) requires zero changes to `Rover`, `Plateau`, `Heading`, or `MissionController` (QS-6 extensibility scenario)
- `MoveForward` holds a reference to `Plateau` so boundary enforcement stays in the domain, never leaking into the adapter (see `04-solution-strategy.md`)
- `TYPE_CHECKING` guard avoids circular imports at runtime while keeping type hints accurate

### Unit tests — `tests/domain/test_commands.py`

```python
from mars_rover.domain.commands import MoveForward, TurnLeft, TurnRight
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


# --- TurnLeft ---

def test_turn_left_changes_heading():
    rover = Rover(0, 0, Heading.N)
    TurnLeft()(rover)
    assert rover.heading == Heading.W


def test_turn_left_does_not_move():
    rover = Rover(2, 3, Heading.N)
    TurnLeft()(rover)
    assert rover.x == 2 and rover.y == 3


# --- TurnRight ---

def test_turn_right_changes_heading():
    rover = Rover(0, 0, Heading.N)
    TurnRight()(rover)
    assert rover.heading == Heading.E


def test_turn_right_does_not_move():
    rover = Rover(2, 3, Heading.N)
    TurnRight()(rover)
    assert rover.x == 2 and rover.y == 3


# --- MoveForward ---

def test_move_forward_north():
    plateau = Plateau(5, 5)
    rover = Rover(1, 2, Heading.N)
    MoveForward(plateau)(rover)
    assert rover.x == 1 and rover.y == 3


def test_move_forward_east():
    plateau = Plateau(5, 5)
    rover = Rover(1, 2, Heading.E)
    MoveForward(plateau)(rover)
    assert rover.x == 2 and rover.y == 2


# --- Kata integration examples ---

def _run(rover: Rover, commands: str, plateau: Plateau) -> Rover:
    mapping = {"L": TurnLeft(), "R": TurnRight(), "M": MoveForward(plateau)}
    for ch in commands:
        rover.execute(mapping[ch])
    return rover


def test_kata_example_1():
    plateau = Plateau(5, 5)
    rover = Rover(1, 2, Heading.N)
    result = _run(rover, "LMLMLMLMM", plateau)
    assert result.x == 1
    assert result.y == 3
    assert result.heading == Heading.N


def test_kata_example_2():
    plateau = Plateau(5, 5)
    rover = Rover(3, 3, Heading.E)
    result = _run(rover, "MMRMMRMRRM", plateau)
    assert result.x == 5
    assert result.y == 1
    assert result.heading == Heading.E
```

---

## Frontend

No UI for this story. Commands are expressed as a plain-text string on stdin:

```
LMLMLMLMM
```

Parsing is covered in STORY-007. Output is covered in STORY-004.

---

## Infrastructure

No infrastructure changes. All command execution is in-memory.

---

## Definition of Done

- [ ] `TurnLeft`, `TurnRight`, `MoveForward` implemented in `mars_rover/domain/commands.py`
- [ ] Both kata integration examples pass (AC-4, AC-5)
- [ ] All individual command unit tests pass
- [ ] `ruff`, `black`, and `isort` pass with no warnings
- [ ] No imports from `adapters/` or `application/` inside `domain/`
