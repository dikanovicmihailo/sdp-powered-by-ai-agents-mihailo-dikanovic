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

**As a** developer **I want** new command types to be deployable by redeploying the Lambda package without any changes to DynamoDB, EventBridge rules, or CloudWatch alarms **so that** extensibility is a pure code-level concern with zero infrastructure impact.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [10-quality-requirements.md](../../architecture/10-quality-requirements.md) — QS-6; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — Command pattern

---

### SCENARIO 1: Adding UTurn requires only a Lambda redeployment — no infrastructure change

**Scenario ID**: NAV-INFRA-004.1-S1

**GIVEN**
* `UTurn` has been added to `commands.py` and registered in `MissionController`

**WHEN**
* `sam deploy` is run to update the Lambda package

**THEN**
* Only the Lambda function code is updated
* The DynamoDB table schema is unchanged
* The EventBridge rules are unchanged
* The CloudWatch alarms are unchanged
* `template.yaml` has zero diff outside the Lambda function code reference

---

### SCENARIO 2: ExecuteCommands Lambda processes a U command from DynamoDB correctly

**Scenario ID**: NAV-INFRA-004.1-S2

**GIVEN**
* A rover record in DynamoDB has `PK=MISSION#abc123`, `SK=ROVER#0`, `x=2`, `y=2`, `heading=N`, `commands="U"`
* The updated Lambda package includes `UTurn`

**WHEN**
* The `ExecuteCommands` Lambda processes the rover

**THEN**
* The domain `MissionController` executes `UTurn` in memory
* The final DynamoDB record has `x=2`, `y=2`, `heading=S`, `status=COMPLETED`
* The `GetMissionResults` Lambda returns `"2 2 S"` for that rover

---

### SCENARIO 3: Unknown command character is rejected at the API layer before Lambda invocation

**Scenario ID**: NAV-INFRA-004.1-S3

**GIVEN**
* The `CreateMission` Lambda validates command strings via `InputParser`
* `InputParser` has been extended to validate that every character in a command string is a registered command letter (requires updating `_parse_commands()` — new method not present in CLI-STORY-001)

**WHEN**
* An operator submits `"commands": "LMX"` (unknown character `X`)

**THEN**
* The Lambda returns HTTP 400: `{ "error": "Unknown command 'X'", "field": "rovers[0].commands" }`
* No DynamoDB write occurs
* No Lambda invocation for `ExecuteCommands` is triggered
* The validation error is logged and counted by the `MarsRover/ValidationErrors` metric

**Required `InputParser` extension:**
```python
# In InputParser — valid commands are injected so the set can be extended
# without modifying InputParser itself (open/closed)
_DEFAULT_VALID_COMMANDS = frozenset("LRM")

class InputParser:
    def __init__(self, valid_commands: frozenset[str] = _DEFAULT_VALID_COMMANDS) -> None:
        self._valid_commands = valid_commands

    def _parse_commands(self, line: str) -> str:
        unknown = [ch for ch in line if ch not in self._valid_commands]
        if unknown:
            raise ValueError(
                f"Unknown command(s) {unknown!r} in command string: {line!r}"
            )
        return line
```

When `UTurn` is registered, the caller constructs `InputParser(valid_commands=frozenset("LRMU"))`. `InputParser` itself is unchanged.

---

### SCENARIO 4: CloudWatch dashboard shows command distribution across missions

**Scenario ID**: NAV-INFRA-004.1-S4

**GIVEN**
* The `ExecuteCommands` Lambda logs each command string length and character distribution

**WHEN**
* The `MarsRoverOps` CloudWatch dashboard is opened

**THEN**
* A widget shows the average command string length per mission over the last 24 hours
* This provides observability into how operators are using the system and whether new commands (like `U`) are being adopted

---

## Definition of Done

- [ ] `UTurn` class added to `mars_rover/domain/commands.py`
- [ ] Command map updated in `MissionController`
- [ ] All 6 `UTurn` unit tests pass
- [ ] Zero changes to `Rover`, `Plateau`, `Heading`, or `OutputFormatter`
- [ ] All existing tests still pass (no regression)
- [ ] `sam deploy` after adding `UTurn` produces zero diff in `template.yaml` outside Lambda code
- [ ] `ExecuteCommands` Lambda processes `U` command from DynamoDB and writes `heading=S` for a north-facing rover
- [ ] Unknown command character rejected at API layer with HTTP 400 before any Lambda invocation
- [ ] `ruff`, `black`, and `isort` pass with no warnings
