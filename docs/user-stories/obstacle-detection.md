# NAV-STORY-003 — Obstacle Detection

## Story

> As an **operator**,
> I want to register obstacles on the plateau,
> so that rovers stop before hitting them and report their last safe position.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `Plateau`, `MoveForward`; [01-introduction.md](../../architecture/01-introduction.md) — FR-7; [06-runtime.md](../../architecture/06-runtime.md) — Scenario 4; [11-risks-and-technical-debts.md](../../architecture/11-risks-and-technical-debts.md) — TD-1; [02-constraints.md](../../architecture/02-constraints.md) — DC-6

---

## Scenarios

### SCENARIO 1: Rover stops before hitting obstacle

**Scenario ID**: NAV-STORY-003-S1

**GIVEN**
* Obstacle at `(2, 2)` and rover at `(1, 2, E)`

**WHEN**
* Command `M` is executed

**THEN**
* Rover stays at `(1, 2, E)` and the mission for that rover ends

---

### SCENARIO 2: Obstacle-stopped rover is marked in output

**Scenario ID**: NAV-STORY-003-S2

**GIVEN**
* Obstacle at `(2, 2)` and rover at `(1, 2, E)`

**WHEN**
* The mission ends

**THEN**
* Output is `O:1 2 E` (obstacle-stop prefix)

---

### SCENARIO 3: No obstacles means normal behavior

**Scenario ID**: NAV-STORY-003-S3

**GIVEN**
* No obstacles are registered

**WHEN**
* A rover moves normally

**THEN**
* Behavior is identical to NAV-STORY-001 and NAV-STORY-002

---

### SCENARIO 4: Remaining commands are skipped after obstacle

**Scenario ID**: NAV-STORY-003-S4

**GIVEN**
* Obstacle at `(2, 2)` and rover receives `MMM`

**WHEN**
* The first `M` is blocked

**THEN**
* Rover stops and remaining commands are not executed

---

## Backend Sub-Story

**Story ID**: NAV-BE-003.1

**As a** developer **I want** `Plateau.is_blocked()` and `ObstacleEncountered` exception **so that** obstacle detection is a domain rule that propagates to the application layer.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `Plateau`, `MoveForward`; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — domain isolation; [11-risks-and-technical-debts.md](../../architecture/11-risks-and-technical-debts.md) — TD-1

**Scenarios:**

### SCENARIO 1: MoveForward raises ObstacleEncountered on blocked cell

**Scenario ID**: NAV-BE-003.1-S1

**GIVEN**
* `Plateau` has obstacles and `MoveForward` would enter a blocked cell

**WHEN**
* `MoveForward` is called

**THEN**
* `ObstacleEncountered` exception is raised
* Rover position is unchanged

---

### SCENARIO 2: MissionController catches exception and stops rover mission

**Scenario ID**: NAV-BE-003.1-S2

**GIVEN**
* A rover encounters an obstacle during its command sequence

**WHEN**
* `MissionController.run()` processes the mission

**THEN**
* The rover's mission stops at the obstacle
* Remaining rovers continue normally

---

### Domain changes — `mars_rover/domain/plateau.py`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Plateau:
    width: int
    height: int
    obstacles: frozenset[tuple[int, int]] = frozenset()

    def is_within(self, x: int, y: int) -> bool:
        return 0 <= x <= self.width and 0 <= y <= self.height

    def is_blocked(self, x: int, y: int) -> bool:
        return (x, y) in self.obstacles
```

### Domain changes — `mars_rover/domain/commands.py`

```python
class ObstacleEncountered(Exception):
    """Raised when MoveForward would enter an obstacle cell."""


class MoveForward:
    def __call__(self, rover: "Rover") -> None:
        dx, dy = rover.heading.delta()
        new_x, new_y = rover.x + dx, rover.y + dy
        if not self._plateau.is_within(new_x, new_y):
            return  # boundary safe-stop
        if self._plateau.is_blocked(new_x, new_y):
            raise ObstacleEncountered()  # caller ends the mission
        rover.x = new_x
        rover.y = new_y
```

### Application changes — `MissionController.run()`

> ⚠️ **Interface change:** `run()` return type changes from `list[Rover]` to `list[tuple[Rover, bool]]`. The `__main__.py` entry point must be updated accordingly (see below).

```python
from mars_rover.domain.commands import ObstacleEncountered

def run(self, missions: Sequence[tuple[Rover, str]]) -> list[tuple[Rover, bool]]:
    command_map = {
        "L": TurnLeft(),
        "R": TurnRight(),
        "M": MoveForward(self._plateau),
    }
    results: list[tuple[Rover, bool]] = []
    for rover, command_string in missions:
        obstacle_stopped = False
        for ch in command_string:
            try:
                rover.execute(command_map[ch])
            except ObstacleEncountered:
                obstacle_stopped = True
                break
        results.append((rover, obstacle_stopped))
    return results
```

### Adapter changes — `OutputFormatter`

```python
def format(self, rover: Rover, obstacle_stopped: bool = False) -> str:
    prefix = "O:" if obstacle_stopped else ""
    return f"{prefix}{rover.x} {rover.y} {rover.heading.value}"
```

### Entry point update — `mars_rover/__main__.py`

```python
# Updated loop to unpack (rover, obstacle_stopped) tuples
for rover, obstacle_stopped in controller.run(missions):
    print(formatter.format(rover, obstacle_stopped=obstacle_stopped))
```

### Unit tests — `tests/domain/test_obstacle.py`

```python
import pytest
from mars_rover.domain.commands import MoveForward, ObstacleEncountered
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


def test_obstacle_stops_rover():
    plateau = Plateau(5, 5, obstacles=frozenset({(2, 2)}))
    rover = Rover(1, 2, Heading.E)
    with pytest.raises(ObstacleEncountered):
        MoveForward(plateau)(rover)
    assert rover.x == 1 and rover.y == 2


def test_no_obstacle_moves_normally():
    plateau = Plateau(5, 5, obstacles=frozenset())
    rover = Rover(1, 2, Heading.E)
    MoveForward(plateau)(rover)
    assert rover.x == 2 and rover.y == 2


def test_obstacle_output_prefix():
    from mars_rover.adapters.output_formatter import OutputFormatter
    rover = Rover(1, 2, Heading.E)
    assert OutputFormatter().format(rover, obstacle_stopped=True) == "O:1 2 E"


def test_mission_stops_at_obstacle_remaining_commands_skipped():
    from mars_rover.application.mission_controller import MissionController
    plateau = Plateau(5, 5, obstacles=frozenset({(2, 2)}))
    rover = Rover(1, 2, Heading.E)
    controller = MissionController(plateau)
    results = controller.run([(rover, "MMM")])
    final_rover, obstacle_stopped = results[0]
    assert obstacle_stopped is True
    assert final_rover.x == 1 and final_rover.y == 2  # never moved
```

---

## Frontend Sub-Story

**Story ID**: NAV-FE-003.1

**As an** operator **I want** to see the `O:` prefix for obstacle-stopped rovers **so that** I can distinguish between normal completion and obstacle encounters.

**Architecture Reference**: [03-context.md](../../architecture/03-context.md) — System → Operator interface

**Scenarios:**

### SCENARIO 1: Obstacle-stopped rover has O: prefix in output

**Scenario ID**: NAV-FE-003.1-S1

**GIVEN**
* One rover is stopped by an obstacle and another completes normally

**WHEN**
* The mission output is produced

**THEN**
* The obstacle-stopped rover line has `O:` prefix
* The normal rover line has no prefix

Example output:
```
O:1 2 E
5 1 E
```

Input format for obstacles is not defined by the original kata — a suggested extension:
```
5 5
2 2
1 2 N
LMLMLMLMM
```
(Second line = obstacle coordinates, one per line before rover blocks.)

---

## Infrastructure Sub-Story

**Story ID**: NAV-INFRA-003.1

**As a** developer **I want** obstacles to be registered in-memory at parse time **so that** no external obstacle service or database is needed.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — single-process CLI, no persistence

**Scenarios:**

### SCENARIO 1: Obstacles are held in memory only

**Scenario ID**: NAV-INFRA-003.1-S1

**GIVEN**
* Obstacles are defined in the input

**WHEN**
* The CLI processes the mission

**THEN**
* Obstacles are stored in the `Plateau` object in memory
* No file, database, or external service is used for obstacle storage

No infrastructure changes. Obstacles are in-memory, registered at parse time.

---

## Definition of Done

- [ ] `Plateau.is_blocked()` implemented
- [ ] `ObstacleEncountered` exception defined in `commands.py`
- [ ] `MissionController` catches `ObstacleEncountered` and stops that rover's mission
- [ ] `OutputFormatter` emits `O:` prefix for obstacle-stopped rovers
- [ ] All obstacle unit tests pass (including mission-level stop test for NAV-STORY-003-S4)
- [ ] Existing boundary and navigation tests still pass (no regression)
- [ ] `ruff`, `black`, and `isort` pass with no warnings
