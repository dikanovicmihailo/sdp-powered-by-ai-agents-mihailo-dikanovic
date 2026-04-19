# NAV-STORY-002 — Boundary Safe-Stop

## Story

> As an **operator**,
> I want a rover that would move off the plateau to stay in place,
> so that it never leaves the grid and the mission always completes normally.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `MoveForward` command; [01-introduction.md](../../architecture/01-introduction.md) — FR-6; [10-quality-requirements.md](../../architecture/10-quality-requirements.md) — QS-3, QS-4; [02-constraints.md](../../architecture/02-constraints.md) — DC-5

---

## Scenarios

### SCENARIO 1: Rover at south boundary stays in place

**Scenario ID**: NAV-STORY-002-S1

**GIVEN**
* A rover at `(0, 0, S)` on plateau `5 5`

**WHEN**
* Command `M` is executed

**THEN**
* Rover stays at `(0, 0, S)` and no exception is raised

---

### SCENARIO 2: Rover at north boundary stays in place

**Scenario ID**: NAV-STORY-002-S2

**GIVEN**
* A rover at `(5, 5, N)` on plateau `5 5`

**WHEN**
* Command `M` is executed

**THEN**
* Rover stays at `(5, 5, N)` and no exception is raised

---

### SCENARIO 3: Rover at west boundary stays in place

**Scenario ID**: NAV-STORY-002-S3

**GIVEN**
* A rover at `(0, 0, W)` on plateau `5 5`

**WHEN**
* Command `M` is executed

**THEN**
* Rover stays at `(0, 0, W)` and no exception is raised

---

### SCENARIO 4: Rover at east boundary stays in place

**Scenario ID**: NAV-STORY-002-S4

**GIVEN**
* A rover at `(5, 0, E)` on plateau `5 5`

**WHEN**
* Command `M` is executed

**THEN**
* Rover stays at `(5, 0, E)` and no exception is raised

---

### SCENARIO 5: Mission continues after a safe-stop

**Scenario ID**: NAV-STORY-002-S5

**GIVEN**
* A rover receives `MMM` but only 1 step is valid

**WHEN**
* All 3 commands execute

**THEN**
* Rover moves 1 step, then stays in place for the remaining 2
* Mission completes normally with no error

---

## Backend Sub-Story

**Story ID**: NAV-BE-002.1

**As a** developer **I want** `MoveForward` to silently ignore out-of-bounds moves **so that** boundary violations never raise exceptions or abort the mission.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `MoveForward`; [08-cross-cutting-concepts.md](../../architecture/08-cross-cutting-concepts.md) — safe-stop contract; [11-risks-and-technical-debts.md](../../architecture/11-risks-and-technical-debts.md) — R-1

**Scenarios:**

### SCENARIO 1: Boundary check is embedded in MoveForward

**Scenario ID**: NAV-BE-002.1-S1

**GIVEN**
* `MoveForward` is called with a rover at a boundary edge

**WHEN**
* The computed next position is outside `Plateau.is_within()`

**THEN**
* The rover's `x` and `y` are not updated
* No exception propagates to the caller

---

The safe-stop behaviour is already encoded in `MoveForward.__call__` (NAV-STORY-001). This story adds explicit tests to verify all four boundary edges and the multi-command continuation behaviour.

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
    rover = Rover(0, 0, Heading.S)
    move = MoveForward(plateau)
    move(rover)           # safe-stop: stays at (0, 0, S)
    TurnRight()(rover)    # now facing W
    TurnRight()(rover)    # now facing N
    move(rover)           # valid move: goes to (0, 1, N)
    assert rover.x == 0 and rover.y == 1 and rover.heading == Heading.N


def test_safe_stop_multiple_blocked_moves(plateau):
    rover = Rover(3, 5, Heading.N)
    move = MoveForward(plateau)
    for _ in range(3):
        move(rover)
    assert rover.x == 3 and rover.y == 5
```

---

## Frontend Sub-Story

**Story ID**: NAV-FE-002.1

**As an** operator **I want** to receive the rover's last safe position when a boundary is hit **so that** I always get a valid result with no special error handling needed.

**Architecture Reference**: [03-context.md](../../architecture/03-context.md) — System → Operator interface

**Scenarios:**

### SCENARIO 1: Boundary safe-stop produces normal output

**Scenario ID**: NAV-FE-002.1-S1

**GIVEN**
* A rover hits a boundary during its command sequence

**WHEN**
* The mission completes

**THEN**
* The operator receives the rover's last valid position in the standard `x y HEADING` format
* No special marker or error message is emitted (contrast with obstacle detection in NAV-STORY-003)

---

## Infrastructure Sub-Story

**Story ID**: NAV-INFRA-002.1

**As a** developer **I want** boundary safe-stop functionality to be containerized and testable **so that** boundary checking works consistently across environments.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [11-risks-and-technical-debts.md](../../architecture/11-risks-and-technical-debts.md) — R-1; [02-constraints.md](../../architecture/02-constraints.md) — DC-5

---

### SCENARIO 1: Container logs boundary safe-stops to stderr with structured metadata

**Scenario ID**: NAV-INFRA-002.1-S1

**GIVEN**
* The Docker container includes boundary checking logic
* A rover at position (0, 0, S) attempts to move forward

**WHEN**
* The container processes the move command

**THEN**
* A structured log is written to stderr indicating the boundary safe-stop
* Log includes rover position, heading, and attempted direction
* Rover position remains unchanged in the final output
* Container continues processing remaining commands

---

### SCENARIO 2: Container handles multiple boundary violations gracefully

**Scenario ID**: NAV-INFRA-002.1-S2

**GIVEN**
* The Docker container processes a command sequence with multiple boundary violations
* Multiple rovers attempt moves outside the plateau

**WHEN**
* The container executes all commands

**THEN**
* Each boundary violation is logged separately to stderr
* All safe-stops are handled without stopping execution
* Final positions reflect only valid moves
* Container completes successfully with exit code 0

---

### SCENARIO 3: Dockerfile builds with boundary checking dependencies

**Scenario ID**: NAV-INFRA-002.1-S3

**GIVEN**
* The boundary checking logic is implemented in domain code
* The Dockerfile includes all domain and application layers

**WHEN**
* `docker build -t mars-rover .` is executed

**THEN**
* The build includes boundary checking code and dependencies
* Plateau boundary validation is available in the container
* The container can perform safe-stop operations correctly
* Build completes without errors

---

### SCENARIO 4: Test suite validates boundary checking inside container

**Scenario ID**: NAV-INFRA-002.1-S4

**GIVEN**
* Test files exist for boundary checking and safe-stop functionality
* The Docker container includes pytest

**WHEN**
* `docker run --rm mars-rover pytest tests/ -k "boundary" -v` is executed

**THEN**
* All 7 boundary tests run inside the container
* Tests validate safe-stop behavior for various boundary conditions
* pytest discovers and executes all boundary-related tests
* Container exits with code 0 on test success

---

## Definition of Done

- [ ] All 7 boundary tests pass
- [ ] No exception is raised on any boundary violation
- [ ] Mission continues normally after a safe-stop (NAV-STORY-002-S5)
- [ ] Container logs boundary safe-stops to stderr with structured metadata
- [ ] Container handles multiple boundary violations gracefully
- [ ] Dockerfile builds successfully with boundary checking dependencies
- [ ] Test suite runs inside container and validates boundary checking
- [ ] `ruff`, `black`, and `isort` pass with no warnings
