# ROVER-STORY-001 — Deploy a Rover

## Story

> As an **operator**,
> I want to deploy a rover at a starting position and heading,
> so that it is ready to receive and execute commands.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `Rover`, `Heading` domain entities; [01-introduction.md](../../architecture/01-introduction.md) — FR-2

---

## Scenarios

### SCENARIO 1: Rover is created with valid position and heading

**Scenario ID**: ROVER-STORY-001-S1

**GIVEN**
* Starting position `1 2 N` is provided

**WHEN**
* A `Rover` is constructed

**THEN**
* `rover.x == 1`, `rover.y == 2`, `rover.heading == Heading.N`

---

### SCENARIO 2: All cardinal headings are accepted

**Scenario ID**: ROVER-STORY-001-S2

**GIVEN**
* Any valid heading (`N`, `E`, `S`, `W`) is provided

**WHEN**
* A `Rover` is constructed

**THEN**
* The heading is stored correctly and readable

---

### SCENARIO 3: Rover state is readable after creation

**Scenario ID**: ROVER-STORY-001-S3

**GIVEN**
* A `Rover(1, 2, Heading.N)` has been created

**WHEN**
* Its state is inspected

**THEN**
* `x`, `y`, and `heading` are all accessible

---

## Backend Sub-Story

**Story ID**: ROVER-BE-001.1

**As a** developer **I want** a mutable `Rover` entity and an immutable `Heading` enum **so that** rover state accumulates correctly as commands are applied.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `Rover`, `Heading`; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — Command pattern

**Scenarios:**

### SCENARIO 1: Heading rotation returns new value without mutation

**Scenario ID**: ROVER-BE-001.1-S1

**GIVEN**
* `Heading.N` exists

**WHEN**
* `turn_left()` is called

**THEN**
* Returns `Heading.W` and the original `Heading.N` is unchanged

---

### SCENARIO 2: Full left-rotation circle returns to origin heading

**Scenario ID**: ROVER-BE-001.1-S2

**GIVEN**
* Starting heading `Heading.N`

**WHEN**
* `turn_left()` is called four times in sequence

**THEN**
* The final heading is `Heading.N`

---

### Domain model — `mars_rover/domain/heading.py`

```python
from enum import Enum


class Heading(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    def turn_left(self) -> "Heading":
        order = [Heading.N, Heading.W, Heading.S, Heading.E]
        return order[(order.index(self) + 1) % 4]

    def turn_right(self) -> "Heading":
        order = [Heading.N, Heading.E, Heading.S, Heading.W]
        return order[(order.index(self) + 1) % 4]

    def delta(self) -> tuple[int, int]:
        """Returns (dx, dy) for one forward step in this heading."""
        return {
            Heading.N: (0, 1),
            Heading.E: (1, 0),
            Heading.S: (0, -1),
            Heading.W: (-1, 0),
        }[self]
```

### Domain model — `mars_rover/domain/rover.py`

```python
from dataclasses import dataclass
from mars_rover.domain.heading import Heading


@dataclass
class Rover:
    """Mutable entity. Accumulates state as commands are applied."""

    x: int
    y: int
    heading: Heading

    def execute(self, command) -> None:
        command(self)
```

**Design notes:**
- `Rover` is intentionally mutable (models a physical vehicle moving through space — see `08-cross-cutting-concepts.md`)
- `execute` accepts any callable that takes a `Rover` — this is the Command pattern (ADR / `04-solution-strategy.md`)
- `Heading` is an immutable enum; rotation methods return new values, never mutate

### Unit tests — `tests/domain/test_rover.py`

```python
from mars_rover.domain.heading import Heading
from mars_rover.domain.rover import Rover


def test_rover_initial_state():
    rover = Rover(1, 2, Heading.N)
    assert rover.x == 1
    assert rover.y == 2
    assert rover.heading == Heading.N


def test_rover_all_headings():
    for heading in Heading:
        rover = Rover(0, 0, heading)
        assert rover.heading == heading
```

### Unit tests — `tests/domain/test_heading.py`

```python
from mars_rover.domain.heading import Heading


def test_turn_left_from_north():
    assert Heading.N.turn_left() == Heading.W


def test_turn_left_full_circle():
    h = Heading.N
    for _ in range(4):
        h = h.turn_left()
    assert h == Heading.N


def test_turn_right_from_north():
    assert Heading.N.turn_right() == Heading.E


def test_turn_right_full_circle():
    h = Heading.N
    for _ in range(4):
        h = h.turn_right()
    assert h == Heading.N


def test_delta_north():
    assert Heading.N.delta() == (0, 1)


def test_delta_east():
    assert Heading.E.delta() == (1, 0)


def test_delta_south():
    assert Heading.S.delta() == (0, -1)


def test_delta_west():
    assert Heading.W.delta() == (-1, 0)
```

---

## Frontend Sub-Story

**Story ID**: ROVER-FE-001.1

**As an** operator **I want** to specify rover deployment via plain-text stdin **so that** I can position a rover without a GUI.

**Architecture Reference**: [03-context.md](../../architecture/03-context.md) — Operator → System interface

**Scenarios:**

### SCENARIO 1: Rover deployment line follows plateau line

**Scenario ID**: ROVER-FE-001.1-S1

**GIVEN**
* The plateau line `5 5` has been read

**WHEN**
* The next line is `1 2 N`

**THEN**
* The system creates `Rover(1, 2, Heading.N)` ready for commands

Rover deployment is expressed via the stdin text format `1 2 N`. Parsing is covered in CLI-STORY-001. Display of the deployed rover's final state is covered in CLI-STORY-002.

---

## Infrastructure Sub-Story

**Story ID**: ROVER-INFRA-001.1

**As a** developer **I want** each rover deployment to be stored as a DynamoDB record and trigger a `RoverDeployed` event **so that** downstream services can react to new rovers without polling the database.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [09-architecture-decisions.md](../../architecture/09-architecture-decisions.md) — ADR-001 DynamoDB single-table design; [02-constraints.md](../../architecture/02-constraints.md) — TC-1

---

### SCENARIO 1: Rover record is written to DynamoDB on deployment

**Scenario ID**: ROVER-INFRA-001.1-S1

**GIVEN**
* A DynamoDB table `MarsRoverMissions` exists
* A mission `abc123` with plateau `5 5` already exists
* `CreateMission` (CLI-INFRA-001.1) calls `DeployRover` internally for each rover in the request

**WHEN**
* The `DeployRover` Lambda is invoked with `missionId=abc123`, `x=1`, `y=2`, `heading=N`, `commands="LMLMLMLMM"`

**THEN**
* A record is written with `PK=MISSION#abc123`, `SK=ROVER#0`, `x=1`, `y=2`, `heading=N`, `commands="LMLMLMLMM"`, `status=DEPLOYED`
* The write succeeds
* The rover index `0` is returned to the caller

**DynamoDB item shape:**
```json
{
  "PK": "MISSION#abc123",
  "SK": "ROVER#0",
  "x": 1,
  "y": 2,
  "heading": "N",
  "commands": "LMLMLMLMM",
  "status": "DEPLOYED"
}
```

> **Note:** `DeployRover` is an internal Lambda, not a public API endpoint. It is invoked by `CreateMission` once per rover in the submitted mission. Operators never call it directly.

---

### SCENARIO 2: RoverDeployed event is published to EventBridge on successful write

**Scenario ID**: ROVER-INFRA-001.1-S2

**GIVEN**
* The `DeployRover` Lambda has written the rover record to DynamoDB

**WHEN**
* The DynamoDB write succeeds

**THEN**
* The Lambda publishes a `RoverDeployed` event to the `MarsRoverEventBus` EventBridge bus
* The event payload includes `missionId`, `roverIndex`, `x`, `y`, `heading`
* Downstream consumers (e.g. a mission status tracker) can subscribe to this event

**EventBridge event shape:**
```json
{
  "source": "mars-rover.deploy",
  "detail-type": "RoverDeployed",
  "detail": {
    "missionId": "abc123",
    "roverIndex": 0,
    "x": 1,
    "y": 2,
    "heading": "N"
  }
}
```

---

### SCENARIO 3: DeployRover Lambda is deployed with least-privilege IAM

**Scenario ID**: ROVER-INFRA-001.1-S3

**GIVEN**
* The `DeployRover` Lambda is defined in `template.yaml`

**WHEN**
* `sam deploy` is run

**THEN**
* The Lambda's IAM role has exactly: `dynamodb:PutItem` on `MarsRoverMissions` and `events:PutEvents` on `MarsRoverEventBus`
* No wildcard (`*`) resource permissions are granted
* The function has a 10-second timeout and 128 MB memory

---

### SCENARIO 4: CloudWatch alarm fires when rover deployment fails

**Scenario ID**: ROVER-INFRA-001.1-S4

**GIVEN**
* A CloudWatch alarm monitors the `DeployRover` Lambda error metric

**WHEN**
* The Lambda fails (e.g. DynamoDB write rejected, EventBridge throttled)

**THEN**
* The `DeployRoverErrors` alarm transitions to `ALARM` within 1 minute
* The error is logged to CloudWatch Logs with `missionId`, `roverIndex`, and the exception type
* The alarm action notifies the ops SNS topic

---

## Definition of Done

- [ ] `Heading` enum implemented in `mars_rover/domain/heading.py`
- [ ] `Rover` dataclass implemented in `mars_rover/domain/rover.py`
- [ ] All heading rotation and delta tests pass
- [ ] All rover initialisation tests pass
- [ ] `DeployRover` Lambda writes rover record to DynamoDB with correct item shape
- [ ] `RoverDeployed` event published to `MarsRoverEventBus` on successful write
- [ ] Lambda IAM role scoped to `dynamodb:PutItem` and `events:PutEvents` only
- [ ] `DeployRoverErrors` CloudWatch alarm defined and wired to SNS topic
- [ ] `ruff`, `black`, and `isort` pass with no warnings
- [ ] No imports from `adapters/` or `application/` inside `domain/`
