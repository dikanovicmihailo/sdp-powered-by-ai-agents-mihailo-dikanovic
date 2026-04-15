# NAV-STORY-001 — Navigate a Rover

## Story

> As an **operator**,
> I want to send a command string of `L`, `R`, and `M` instructions to a rover,
> so that it navigates the plateau and reaches its intended destination.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `Command` protocol, `TurnLeft`, `TurnRight`, `MoveForward`; [01-introduction.md](../../architecture/01-introduction.md) — FR-3; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — Command pattern

---

## Scenarios

### SCENARIO 1: Turn left changes heading

**Scenario ID**: NAV-STORY-001-S1

**GIVEN**
* A rover at `(1, 2, N)`

**WHEN**
* Command `L` is executed

**THEN**
* Rover is at `(1, 2, W)`

---

### SCENARIO 2: Turn right changes heading

**Scenario ID**: NAV-STORY-001-S2

**GIVEN**
* A rover at `(1, 2, N)`

**WHEN**
* Command `R` is executed

**THEN**
* Rover is at `(1, 2, E)`

---

### SCENARIO 3: Move forward advances position

**Scenario ID**: NAV-STORY-001-S3

**GIVEN**
* A rover at `(1, 2, N)` on plateau `5 5`

**WHEN**
* Command `M` is executed

**THEN**
* Rover is at `(1, 3, N)`

---

### SCENARIO 4: Kata example 1 — full command string

**Scenario ID**: NAV-STORY-001-S4

**GIVEN**
* A rover at `(1, 2, N)` on plateau `5 5`

**WHEN**
* Command string `LMLMLMLMM` is executed

**THEN**
* Rover ends at `(1, 3, N)`

---

### SCENARIO 5: Kata example 2 — full command string

**Scenario ID**: NAV-STORY-001-S5

**GIVEN**
* A rover at `(3, 3, E)` on plateau `5 5`

**WHEN**
* Command string `MMRMMRMRRM` is executed

**THEN**
* Rover ends at `(5, 1, E)`

---

## Backend Sub-Story

**Story ID**: NAV-BE-001.1

**As a** developer **I want** `TurnLeft`, `TurnRight`, and `MoveForward` command objects **so that** each instruction is an isolated, testable callable that transforms rover state.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `Command` protocol; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — Command pattern (open/closed principle)

**Scenarios:**

### SCENARIO 1: TurnLeft does not move the rover

**Scenario ID**: NAV-BE-001.1-S1

**GIVEN**
* A rover at `(2, 3, N)`

**WHEN**
* `TurnLeft()` is called

**THEN**
* `rover.x == 2` and `rover.y == 3` (position unchanged)
* `rover.heading == Heading.W`

---

### SCENARIO 2: MoveForward uses plateau boundary check

**Scenario ID**: NAV-BE-001.1-S2

**GIVEN**
* A `Plateau(5, 5)` and a rover at `(1, 2, N)`

**WHEN**
* `MoveForward(plateau)` is called

**THEN**
* Rover moves to `(1, 3, N)`

---

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
        # else: safe-stop — position unchanged (see NAV-STORY-002)
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


def test_turn_left_changes_heading():
    rover = Rover(0, 0, Heading.N)
    TurnLeft()(rover)
    assert rover.heading == Heading.W


def test_turn_left_does_not_move():
    rover = Rover(2, 3, Heading.N)
    TurnLeft()(rover)
    assert rover.x == 2 and rover.y == 3


def test_turn_right_changes_heading():
    rover = Rover(0, 0, Heading.N)
    TurnRight()(rover)
    assert rover.heading == Heading.E


def test_turn_right_does_not_move():
    rover = Rover(2, 3, Heading.N)
    TurnRight()(rover)
    assert rover.x == 2 and rover.y == 3


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


def _run(rover, commands, plateau):
    mapping = {"L": TurnLeft(), "R": TurnRight(), "M": MoveForward(plateau)}
    for ch in commands:
        rover.execute(mapping[ch])
    return rover


def test_kata_example_1():
    plateau = Plateau(5, 5)
    rover = Rover(1, 2, Heading.N)
    result = _run(rover, "LMLMLMLMM", plateau)
    assert result.x == 1 and result.y == 3 and result.heading == Heading.N


def test_kata_example_2():
    plateau = Plateau(5, 5)
    rover = Rover(3, 3, Heading.E)
    result = _run(rover, "MMRMMRMRRM", plateau)
    assert result.x == 5 and result.y == 1 and result.heading == Heading.E
```

---

## Frontend Sub-Story

**Story ID**: NAV-FE-001.1

**As an** operator **I want** to express commands as a plain-text string on stdin **so that** I can navigate a rover without a GUI.

**Architecture Reference**: [03-context.md](../../architecture/03-context.md) — Operator → System interface

**Scenarios:**

### SCENARIO 1: Command string follows rover deployment line

**Scenario ID**: NAV-FE-001.1-S1

**GIVEN**
* The rover deployment line `1 2 N` has been read

**WHEN**
* The next line is `LMLMLMLMM`

**THEN**
* The system executes each character as a command in order

Commands are expressed as a plain-text string on stdin. Parsing is covered in CLI-STORY-001. Output is covered in CLI-STORY-002.

---

## Infrastructure Sub-Story

**Story ID**: NAV-INFRA-001.1

**As a** developer **I want** all command execution to be in-memory **so that** no external resources are needed during navigation.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — single-process CLI, no persistence

**Scenarios:**

### SCENARIO 1: Command execution requires no I/O

**Scenario ID**: NAV-INFRA-001.1-S1

**GIVEN**
* A rover and a command string are in memory

**WHEN**
* Each command is executed

**THEN**
* No file, database, or network call is made
* All state changes are confined to the `Rover` object in memory

No infrastructure changes. All command execution is in-memory.

---

## Definition of Done

- [ ] `TurnLeft`, `TurnRight`, `MoveForward` implemented in `mars_rover/domain/commands.py`
- [ ] Both kata integration examples pass (NAV-STORY-001-S4, NAV-STORY-001-S5)
- [ ] All individual command unit tests pass
- [ ] `ruff`, `black`, and `isort` pass with no warnings
- [ ] No imports from `adapters/` or `application/` inside `domain/`
