# STORY-006 — Multi-Rover Mission

## Story

> As an **operator**,
> I want to deploy multiple rovers in a single mission,
> so that I can navigate all of them with one invocation and receive all their final positions.

---

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC-1 | Two rovers with separate command strings | Mission runs | Each rover processes its own commands independently |
| AC-2 | Rover 1 finishes | Rover 2 starts | Rover 2 is unaffected by Rover 1's final state |
| AC-3 | Two rovers complete | Output is produced | Two lines, one per rover, in deployment order |
| AC-4 | Kata full example (rovers 1 and 2) | Mission runs | Output is `1 3 N` then `5 1 E` |

---

## Architecture References

- **FR-4** — rovers processed sequentially; a rover completes all commands before the next starts
- **DC-4** — sequential processing assumption (no concurrent movement)
- **R-3** — risk: simultaneous movement not supported; document assumption explicitly
- Component: `application/mission_controller.py` → `MissionController`

---

## Backend

### Application layer — `mars_rover/application/mission_controller.py`

```python
from mars_rover.domain.rover import Rover
from mars_rover.domain.commands import TurnLeft, TurnRight, MoveForward
from mars_rover.domain.plateau import Plateau
from typing import Sequence


class MissionController:
    def __init__(self, plateau: Plateau) -> None:
        self._plateau = plateau

    def run(self, missions: Sequence[tuple[Rover, str]]) -> list[Rover]:
        """
        Execute all rover missions sequentially.

        :param missions: Ordered list of (rover, command_string) pairs.
        :returns: The same rovers in order, with their final state applied.
        """
        command_map = {
            "L": TurnLeft(),
            "R": TurnRight(),
            "M": MoveForward(self._plateau),
        }
        for rover, command_string in missions:
            for ch in command_string:
                rover.execute(command_map[ch])
        return [rover for rover, _ in missions]
```

**Design notes:**
- `MissionController` owns the command-string → command-object mapping; `InputParser` (STORY-007) produces raw strings, keeping parsing out of the application layer
- `MoveForward` is instantiated once per plateau and reused across all rovers — safe because it holds no per-rover state
- Sequential processing is explicit and documented (DC-4); no thread safety required

### Unit tests — `tests/application/test_mission_controller.py`

```python
from mars_rover.application.mission_controller import MissionController
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


def test_single_rover_kata_example_1():
    plateau = Plateau(5, 5)
    rover = Rover(1, 2, Heading.N)
    controller = MissionController(plateau)
    results = controller.run([(rover, "LMLMLMLMM")])
    assert results[0].x == 1
    assert results[0].y == 3
    assert results[0].heading == Heading.N


def test_single_rover_kata_example_2():
    plateau = Plateau(5, 5)
    rover = Rover(3, 3, Heading.E)
    controller = MissionController(plateau)
    results = controller.run([(rover, "MMRMMRMRRM")])
    assert results[0].x == 5
    assert results[0].y == 1
    assert results[0].heading == Heading.E


def test_full_kata_two_rovers():
    plateau = Plateau(5, 5)
    missions = [
        (Rover(1, 2, Heading.N), "LMLMLMLMM"),
        (Rover(3, 3, Heading.E), "MMRMMRMRRM"),
    ]
    controller = MissionController(plateau)
    results = controller.run(missions)
    assert results[0].x == 1 and results[0].y == 3 and results[0].heading == Heading.N
    assert results[1].x == 5 and results[1].y == 1 and results[1].heading == Heading.E


def test_rovers_are_independent():
    """Rover 1 ending at (5, 5) has no effect on Rover 2 starting at (0, 0)."""
    plateau = Plateau(5, 5)
    rover1 = Rover(5, 5, Heading.N)
    rover2 = Rover(0, 0, Heading.E)
    controller = MissionController(plateau)
    results = controller.run([(rover1, ""), (rover2, "M")])
    assert results[1].x == 1 and results[1].y == 0


def test_empty_command_string_leaves_rover_unchanged():
    plateau = Plateau(5, 5)
    rover = Rover(2, 3, Heading.W)
    controller = MissionController(plateau)
    results = controller.run([(rover, "")])
    assert results[0].x == 2 and results[0].y == 3 and results[0].heading == Heading.W
```

---

## Frontend

No UI impact. The operator provides multiple rover blocks in the stdin input:

```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

And receives one output line per rover:

```
1 3 N
5 1 E
```

---

## Infrastructure

No infrastructure changes. All rovers run in the same single process, sequentially.

---

## Definition of Done

- [ ] `MissionController` implemented in `mars_rover/application/mission_controller.py`
- [ ] Full kata two-rover test passes (AC-4)
- [ ] Rover independence test passes (AC-2)
- [ ] `ruff`, `black`, and `isort` pass with no warnings
- [ ] `MissionController` does not import from `adapters/`
