# MISSION-STORY-001 — Multi-Rover Mission

## Story

> As an **operator**,
> I want to deploy multiple rovers in a single mission,
> so that I can navigate all of them with one invocation and receive all their final positions.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `MissionController` application layer; [01-introduction.md](../../architecture/01-introduction.md) — FR-4; [02-constraints.md](../../architecture/02-constraints.md) — DC-4

---

## Scenarios

### SCENARIO 1: Each rover processes its own commands independently

**Scenario ID**: MISSION-STORY-001-S1

**GIVEN**
* Two rovers with separate command strings are provided

**WHEN**
* The mission runs

**THEN**
* Each rover processes its own commands without interference from the other

---

### SCENARIO 2: Rover 2 is unaffected by Rover 1's final state

**Scenario ID**: MISSION-STORY-001-S2

**GIVEN**
* Rover 1 finishes at any position

**WHEN**
* Rover 2 starts

**THEN**
* Rover 2 begins from its own initial position, unaffected by Rover 1

---

### SCENARIO 3: Output contains one line per rover in deployment order

**Scenario ID**: MISSION-STORY-001-S3

**GIVEN**
* Two rovers complete their missions

**WHEN**
* Output is produced

**THEN**
* Two lines appear on stdout, one per rover, in deployment order

---

### SCENARIO 4: Full kata two-rover example

**Scenario ID**: MISSION-STORY-001-S4

**GIVEN**
* Plateau `5 5`, Rover 1 at `(1, 2, N)` with commands `LMLMLMLMM`, Rover 2 at `(3, 3, E)` with commands `MMRMMRMRRM`

**WHEN**
* The mission runs

**THEN**
* Output is `1 3 N` then `5 1 E`

---

## Backend Sub-Story

**Story ID**: MISSION-BE-001.1

**As a** developer **I want** a `MissionController` that orchestrates sequential rover execution **so that** the application layer coordinates missions without knowing domain internals.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `MissionController`; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — Hexagonal architecture; [02-constraints.md](../../architecture/02-constraints.md) — DC-4 sequential processing

**Scenarios:**

### SCENARIO 1: MissionController does not import from adapters

**Scenario ID**: MISSION-BE-001.1-S1

**GIVEN**
* `MissionController` is implemented

**WHEN**
* Its imports are inspected

**THEN**
* No import from `mars_rover.adapters` exists

---

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
- `MissionController` owns the command-string → command-object mapping; `InputParser` (CLI-STORY-001) produces raw strings, keeping parsing out of the application layer
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
    assert results[0].x == 1 and results[0].y == 3 and results[0].heading == Heading.N


def test_single_rover_kata_example_2():
    plateau = Plateau(5, 5)
    rover = Rover(3, 3, Heading.E)
    controller = MissionController(plateau)
    results = controller.run([(rover, "MMRMMRMRRM")])
    assert results[0].x == 5 and results[0].y == 1 and results[0].heading == Heading.E


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

## Frontend Sub-Story

**Story ID**: MISSION-FE-001.1

**As an** operator **I want** to provide multiple rover blocks in a single stdin input **so that** I can run a full multi-rover mission with one command.

**Architecture Reference**: [03-context.md](../../architecture/03-context.md) — Operator → System interface

**Scenarios:**

### SCENARIO 1: Multiple rover blocks are accepted in one input

**Scenario ID**: MISSION-FE-001.1-S1

**GIVEN**
* The operator pipes input with plateau + two rover blocks

**WHEN**
* The CLI runs

**THEN**
* Both rovers are processed and two output lines appear on stdout

Input format:
```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

Expected output:
```
1 3 N
5 1 E
```

---

## Infrastructure Sub-Story

**Story ID**: MISSION-INFRA-001.1

**As a** developer **I want** all rovers to run in the same single process sequentially **so that** no concurrency, queuing, or inter-process communication is needed.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — single-process CLI; [02-constraints.md](../../architecture/02-constraints.md) — DC-4 sequential processing; [11-risks-and-technical-debts.md](../../architecture/11-risks-and-technical-debts.md) — R-3

**Scenarios:**

### SCENARIO 1: Sequential execution requires no concurrency infrastructure

**Scenario ID**: MISSION-INFRA-001.1-S1

**GIVEN**
* Multiple rovers are in the mission

**WHEN**
* The mission runs

**THEN**
* Rovers execute one at a time in a single thread
* No message queue, thread pool, or async runtime is used

No infrastructure changes. All rovers run in the same single process, sequentially.

---

## Definition of Done

- [ ] `MissionController` implemented in `mars_rover/application/mission_controller.py`
- [ ] Full kata two-rover test passes (MISSION-STORY-001-S4)
- [ ] Rover independence test passes (MISSION-STORY-001-S2)
- [ ] `ruff`, `black`, and `isort` pass with no warnings
- [ ] `MissionController` does not import from `adapters/`
