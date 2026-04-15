# STORY-009 — Obstacle Detection

## Story

> As an **operator**,
> I want to register obstacles on the plateau,
> so that rovers stop before hitting them and report their last safe position.

---

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC-1 | Obstacle at `(2, 2)`, rover at `(1, 2, E)` | Command `M` | Rover stays at `(1, 2, E)`; mission for that rover ends |
| AC-2 | Obstacle at `(2, 2)`, rover at `(1, 2, E)` | Mission ends | Output is `O:1 2 E` (obstacle-stop prefix) |
| AC-3 | No obstacles | Rover moves normally | Behaviour identical to STORY-003 / STORY-005 |
| AC-4 | Obstacle at `(2, 2)`, rover receives `MMM` | First `M` is blocked | Rover stops; remaining commands are not executed |

---

## Architecture References

- **FR-7** — optional extension: obstacle detection
- **TD-1** — technical debt: `Plateau.is_within()` only checks boundaries; `is_blocked()` not yet implemented
- **06-runtime.md** — Scenario 4: obstacle detected
- **DC-6** — rover stops before obstacle and reports last safe position

---

## Backend

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
    """AC-4: rover receives MMM, first M is blocked — remaining two are not executed."""
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

## Frontend

The operator sees the `O:` prefix on the output line for any rover that was stopped by an obstacle:

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

## Infrastructure

No infrastructure changes. Obstacles are in-memory, registered at parse time.

---

## Definition of Done

- [ ] `Plateau.is_blocked()` implemented
- [ ] `ObstacleEncountered` exception defined in `commands.py`
- [ ] `MissionController` catches `ObstacleEncountered` and stops that rover's mission
- [ ] `OutputFormatter` emits `O:` prefix for obstacle-stopped rovers
- [ ] All obstacle unit tests pass (including mission-level stop test for AC-4)
- [ ] Existing boundary and navigation tests still pass (no regression)
- [ ] `ruff`, `black`, and `isort` pass with no warnings
