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

**As a** developer **I want** boundary safe-stop events to be logged to CloudWatch with structured metadata **so that** operators can detect misconfigured plateaus by querying logs rather than inspecting raw output.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [11-risks-and-technical-debts.md](../../architecture/11-risks-and-technical-debts.md) — R-1; [02-constraints.md](../../architecture/02-constraints.md) — DC-5

---

### SCENARIO 1: ExecuteCommands Lambda emits a structured log on every boundary safe-stop

**Scenario ID**: NAV-INFRA-002.1-S1

**GIVEN**
* The `ExecuteCommands` Lambda is processing a rover at `(0, 0, S)` with command `M`

**WHEN**
* `MoveForward` applies the safe-stop (position unchanged)

**THEN**
* The Lambda emits a structured log line to CloudWatch Logs:
  ```json
  {
    "level": "WARN",
    "event": "BoundarySafeStop",
    "missionId": "abc123",
    "roverIndex": 0,
    "x": 0,
    "y": 0,
    "heading": "S",
    "attemptedDirection": "S"
  }
  ```
* The rover's final DynamoDB record still reflects the last valid position

---

### SCENARIO 2: CloudWatch Logs Insights query identifies missions with boundary violations

**Scenario ID**: NAV-INFRA-002.1-S2

**GIVEN**
* Multiple Lambda invocations have emitted `BoundarySafeStop` log events

**WHEN**
* An operator runs the following CloudWatch Logs Insights query:
  ```
  fields missionId, roverIndex, x, y, heading
  | filter event = "BoundarySafeStop"
  | stats count(*) as violations by missionId
  | sort violations desc
  ```

**THEN**
* The query returns a table of missions ordered by boundary violation count
* This allows operators to identify misconfigured plateaus without re-running missions

---

### SCENARIO 3: CloudWatch metric filter counts boundary safe-stops per minute

**Scenario ID**: NAV-INFRA-002.1-S3

**GIVEN**
* A CloudWatch metric filter is defined on the `ExecuteCommands` log group

**WHEN**
* A `BoundarySafeStop` log event is emitted

**THEN**
* The custom metric `MarsRover/BoundarySafeStops` is incremented by 1
* The metric is visible in the `MarsRoverOps` CloudWatch dashboard

**Metric filter (SAM):**
```yaml
BoundarySafeStopMetricFilter:
  Type: AWS::Logs::MetricFilter
  Properties:
    LogGroupName: !Sub "/aws/lambda/${ExecuteCommandsFunction}"
    FilterPattern: '{ $.event = "BoundarySafeStop" }'
    MetricTransformations:
      - MetricName: BoundarySafeStops
        MetricNamespace: MarsRover
        MetricValue: "1"
```

---

### SCENARIO 4: CloudWatch alarm fires when safe-stop rate is abnormally high

**Scenario ID**: NAV-INFRA-002.1-S4

**GIVEN**
* The `MarsRover/BoundarySafeStops` custom metric is being published

**WHEN**
* More than 10 safe-stops occur within a 5-minute window

**THEN**
* The `HighBoundarySafeStopRate` alarm transitions to `ALARM`
* An SNS notification is sent to the ops team
* This signals a likely misconfigured plateau that needs operator attention

**CloudWatch alarm (SAM):**
```yaml
HighBoundarySafeStopRateAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: HighBoundarySafeStopRate
    MetricName: BoundarySafeStops
    Namespace: MarsRover
    Statistic: Sum
    Period: 300
    EvaluationPeriods: 1
    Threshold: 10
    ComparisonOperator: GreaterThanThreshold
    AlarmActions:
      - !Ref OpsAlertTopic
```

---

## Definition of Done

- [ ] All 7 boundary tests pass
- [ ] No exception is raised on any boundary violation
- [ ] Mission continues normally after a safe-stop (NAV-STORY-002-S5)
- [ ] `ExecuteCommands` Lambda emits structured `BoundarySafeStop` log on every safe-stop
- [ ] CloudWatch Logs Insights query documented and verified against sample log data
- [ ] `BoundarySafeStopMetricFilter` defined in `template.yaml`; metric increments on each safe-stop
- [ ] `HighBoundarySafeStopRate` alarm defined; fires when > 10 safe-stops in 5 minutes
- [ ] `ruff`, `black`, and `isort` pass with no warnings