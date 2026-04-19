# NAV-STORY-004 — Extensible Command Types

## Story

> As a **developer**,
> I want to add a new command type without modifying existing domain classes,
> so that the system is open for extension and closed for modification.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `Command` protocol; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — Command pattern; [10-quality-requirements.md](../../architecture/10-quality-requirements.md) — QS-6; [08-cross-cutting-concepts.md](../../architecture/08-cross-cutting-concepts.md) — open/closed principle

---

## Scenarios

### SCENARIO 1: New UTurn command rotates rover 180°

**Scenario ID**: NAV-STORY-004-S1

**GIVEN**
* A new `UTurn` command (`U`) is added

**WHEN**
* `UTurn()(rover)` is called

**THEN**
* Rover heading rotates 180° in place

---

### SCENARIO 2: Existing domain classes are unchanged

**Scenario ID**: NAV-STORY-004-S2

**GIVEN**
* `UTurn` is added

**WHEN**
* `Rover`, `Plateau`, `Heading`, `OutputFormatter` source files are inspected

**THEN**
* Zero lines are changed in any of those files

---

### SCENARIO 3: UTurn is dispatched correctly via command map

**Scenario ID**: NAV-STORY-004-S3

**GIVEN**
* `MissionController` command map is updated with `"U": UTurn()`

**WHEN**
* Input string `U` is parsed

**THEN**
* `UTurn` is dispatched correctly

---

### SCENARIO 4: Existing tests pass without modification

**Scenario ID**: NAV-STORY-004-S4

**GIVEN**
* `UTurn` is added

**WHEN**
* Existing tests are run

**THEN**
* All pass without modification

---

## Backend Sub-Story

**Story ID**: NAV-BE-004.1

**As a** developer **I want** the Command pattern to enable adding new commands with zero changes to existing domain logic **so that** the open/closed principle is enforced by the architecture.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `Command` protocol; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — Command pattern; [10-quality-requirements.md](../../architecture/10-quality-requirements.md) — QS-6

**Scenarios:**

### SCENARIO 1: UTurn implements the Command protocol

**Scenario ID**: NAV-BE-004.1-S1

**GIVEN**
* `UTurn` is implemented as a callable class

**WHEN**
* `rover.execute(UTurn())` is called

**THEN**
* The rover's heading changes by 180° and position remains unchanged

---

### SCENARIO 2: UTurn uses existing Heading rotation methods

**Scenario ID**: NAV-BE-004.1-S2

**GIVEN**
* `UTurn` needs to rotate 180°

**WHEN**
* `UTurn.__call__()` is implemented

**THEN**
* It uses `heading.turn_right().turn_right()` (two consecutive right turns)

---

### New command — `mars_rover/domain/commands.py` (append only)

```python
class UTurn:
    """Rotate the rover 180° in place. U = two consecutive right turns."""

    def __call__(self, rover: "Rover") -> None:
        rover.heading = rover.heading.turn_right().turn_right()
```

### Command map update — `mars_rover/application/mission_controller.py`

The only change outside `commands.py` is registering the new letter in the command map inside `MissionController`:

```python
# In MissionController.__init__ or wherever the map lives:
command_map = {
    "L": TurnLeft(),
    "R": TurnRight(),
    "M": MoveForward(self._plateau),
    "U": UTurn(),          # ← only addition required
}
```

### Unit tests — `tests/domain/test_extensible_commands.py`

```python
from mars_rover.domain.commands import UTurn
from mars_rover.domain.heading import Heading
from mars_rover.domain.rover import Rover


def test_uturn_from_north():
    rover = Rover(0, 0, Heading.N)
    UTurn()(rover)
    assert rover.heading == Heading.S


def test_uturn_from_east():
    rover = Rover(0, 0, Heading.E)
    UTurn()(rover)
    assert rover.heading == Heading.W


def test_uturn_from_south():
    rover = Rover(0, 0, Heading.S)
    UTurn()(rover)
    assert rover.heading == Heading.N


def test_uturn_from_west():
    rover = Rover(0, 0, Heading.W)
    UTurn()(rover)
    assert rover.heading == Heading.E


def test_uturn_does_not_move():
    rover = Rover(3, 4, Heading.N)
    UTurn()(rover)
    assert rover.x == 3 and rover.y == 4


def test_uturn_via_rover_execute():
    rover = Rover(0, 0, Heading.N)
    rover.execute(UTurn())
    assert rover.heading == Heading.S
```

### Proof of open/closed compliance

Files touched to add `UTurn`:

| File | Change |
|------|--------|
| `mars_rover/domain/commands.py` | Add `UTurn` class (new code only) |
| `mars_rover/application/mission_controller.py` | Add `"U": UTurn()` to command map |
| `tests/domain/test_extensible_commands.py` | New test file |

Files **not** touched:

- `mars_rover/domain/rover.py` ✅
- `mars_rover/domain/plateau.py` ✅
- `mars_rover/domain/heading.py` ✅
- `mars_rover/adapters/input_parser.py` ✅
- `mars_rover/adapters/output_formatter.py` ✅

---

## Frontend Sub-Story

**Story ID**: NAV-FE-004.1

**As an** operator **I want** to include `U` in command strings once the mapping is registered **so that** I can use the new command without changing my input format.

**Architecture Reference**: [03-context.md](../../architecture/03-context.md) — Operator → System interface

**Scenarios:**

### SCENARIO 1: U command is accepted in input strings

**Scenario ID**: NAV-FE-004.1-S1

**GIVEN**
* `UTurn` is registered in the command map

**WHEN**
* The operator includes `U` in a command string

**THEN**
* The rover executes a 180° turn at that point in the sequence

No UI impact. The operator can include `U` in any command string once the mapping is registered.

---

## Infrastructure Sub-Story

**Story ID**: NAV-INFRA-004.1

**As a** developer **I want** extensible command functionality to be containerized and testable **so that** new commands can be added and validated consistently across environments.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [10-quality-requirements.md](../../architecture/10-quality-requirements.md) — QS-6; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — Command pattern

---

### SCENARIO 1: Container processes new UTurn command correctly

**Scenario ID**: NAV-INFRA-004.1-S1

**GIVEN**
* The Docker container includes UTurn command implementation
* Input contains a rover with command string including "U"

**WHEN**
* The container processes the mission

**THEN**
* UTurn command is executed correctly (180-degree rotation)
* Final rover position reflects the UTurn operation
* Container completes successfully with correct output
* No errors are logged for the UTurn command

---

### SCENARIO 2: Container validates command strings and rejects unknown commands

**Scenario ID**: NAV-INFRA-004.1-S2

**GIVEN**
* The Docker container includes command validation logic
* Input contains an unknown command character "X"

**WHEN**
* The container processes the input

**THEN**
* Validation error is logged to stderr with unknown command details
* Container exits with non-zero exit code
* No processing of invalid commands occurs
* Error message indicates which command character is invalid

---

### SCENARIO 3: Dockerfile builds with extensible command dependencies

**Scenario ID**: NAV-INFRA-004.1-S3

**GIVEN**
* The extensible command system is implemented in domain code
* The Dockerfile includes all command implementations

**WHEN**
* `docker build -t mars-rover .` is executed

**THEN**
* The build includes all command classes and the command registry
* UTurn and other extensible commands are available in the container
* The container can execute any registered command
* Build completes without errors

---

### SCENARIO 4: Test suite validates extensible commands inside container

**Scenario ID**: NAV-INFRA-004.1-S4

**GIVEN**
* Test files exist for extensible command functionality including UTurn
* The Docker container includes pytest

**WHEN**
* `docker run --rm mars-rover pytest tests/ -k "command" -v` is executed

**THEN**
* All extensible command tests run inside the container
* Tests validate UTurn functionality and command validation
* pytest discovers and executes all command-related tests
* Container exits with code 0 on test success

---

## Definition of Done

- [ ] `UTurn` class added to `mars_rover/domain/commands.py`
- [ ] Command map updated in `MissionController`
- [ ] All 6 `UTurn` unit tests pass
- [ ] Zero changes to `Rover`, `Plateau`, `Heading`, or `OutputFormatter`
- [ ] All existing tests still pass (no regression)
- [ ] Container processes new UTurn command correctly
- [ ] Container validates command strings and rejects unknown commands
- [ ] Dockerfile builds successfully with extensible command dependencies
- [ ] Test suite runs inside container and validates extensible commands
- [ ] `ruff`, `black`, and `isort` pass with no warnings
