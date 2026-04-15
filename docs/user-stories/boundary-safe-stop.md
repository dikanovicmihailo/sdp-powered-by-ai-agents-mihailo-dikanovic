# STORY-005 — Boundary Safe-Stop

## Story

> As an **operator**,
> I want a rover that would move off the plateau to stay in place,
> so that it never leaves the grid and the mission always completes normally.

---

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC-1 | Rover at `(0, 0, S)` on plateau `5 5` | Command `M` is executed | Rover stays at `(0, 0, S)`; no exception raised |
| AC-2 | Rover at `(5, 5, N)` on plateau `5 5` | Command `M` is executed | Rover stays at `(5, 5, N)`; no exception raised |
| AC-3 | Rover at `(0, 0, W)` on plateau `5 5` | Command `M` is executed | Rover stays at `(0, 0, W)`; no exception raised |
| AC-4 | Rover at `(5, 0, E)` on plateau `5 5` | Command `M` is executed | Rover stays at `(5, 0, E)`; no exception raised |
| AC-5 | Rover receives `MMM` but only 1 step is valid | All 3 commands execute | Rover moves 1 step, then stays in place for the remaining 2; mission completes |

---

## Architecture References

- **FR-6** — rover must not move outside plateau boundaries
- **DC-5** — safe-stop: rover stays in place, no error raised
- **QS-3 / QS-4** — boundary safety quality scenarios from `10-quality-requirements.md`
- **R-1** — risk: silent boundary violations could mask misconfiguration
- Component: `domain/commands.py` → `MoveForward` (boundary check already embedded — see STORY-003)

---

## Backend

The safe-stop behaviour is already encoded in `MoveForward.__call__` (STORY-003). This story adds explicit tests to verify all four boundary edges and the multi-command continuation behaviour.

No new production code is required — this story is fully covered by tests.

### Unit tests — `tests/domain/test_boundary.py`

```python
import pytest
from mars_rover.domain.commands import MoveForward, TurnRight
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


@pytest.fixture
def plateau():
    return Plateau(5, 5)


def test_safe_stop_south_boundary(plateau):
    rover = Rover(0, 0, Heading.S)
    MoveForward(plateau)(rover)
    assert rover.x == 0 and rover.y == 0


def test_safe_stop_north_boundary(plateau):
    rover = Rover(5, 5, Heading.N)
    MoveForward(plateau)(rover)
    assert rover.x == 5 and rover.y == 5


def test_safe_stop_west_boundary(plateau):
    rover = Rover(0, 0, Heading.W)
    MoveForward(plateau)(rover)
    assert rover.x == 0 and rover.y == 0


def test_safe_stop_east_boundary(plateau):
    rover = Rover(5, 0, Heading.E)
    MoveForward(plateau)(rover)
    assert rover.x == 5 and rover.y == 0


def test_safe_stop_does_not_raise(plateau):
    rover = Rover(0, 0, Heading.S)
    try:
        MoveForward(plateau)(rover)
    except Exception as exc:
        pytest.fail(f"MoveForward raised unexpectedly: {exc}")


def test_safe_stop_allows_subsequent_commands(plateau):
    """Rover at south boundary: M is ignored, then R turns it east, then M moves it."""
    rover = Rover(0, 0, Heading.S)
    move = MoveForward(plateau)
    move(rover)           # safe-stop: stays at (0, 0, S)
    TurnRight()(rover)    # now facing W
    TurnRight()(rover)    # now facing N
    move(rover)           # valid move: goes to (0, 1, N)
    assert rover.x == 0 and rover.y == 1 and rover.heading == Heading.N


def test_safe_stop_multiple_blocked_moves(plateau):
    """Three forward commands from the north edge — all three are no-ops."""
    rover = Rover(3, 5, Heading.N)
    move = MoveForward(plateau)
    for _ in range(3):
        move(rover)
    assert rover.x == 3 and rover.y == 5
```

---

## Frontend

No UI impact. The operator simply receives the rover's last safe position in the normal output format (STORY-004). No special marker is emitted for a boundary safe-stop (contrast with obstacle detection in STORY-009).

---

## Infrastructure

No infrastructure changes.

---

## Definition of Done

- [ ] All 7 boundary tests pass
- [ ] No exception is raised on any boundary violation
- [ ] Mission continues normally after a safe-stop (AC-5)
- [ ] `ruff`, `black`, and `isort` pass with no warnings
