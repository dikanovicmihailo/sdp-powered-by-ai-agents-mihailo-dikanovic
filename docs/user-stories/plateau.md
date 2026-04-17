# PLATEAU-STORY-001 — Define the Plateau

## Story

> As an **operator**,
> I want to define a rectangular plateau by its upper-right corner coordinates,
> so that rovers have a bounded grid to navigate within.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `Plateau` domain value object; [01-introduction.md](../../architecture/01-introduction.md) — FR-1

---

## Scenarios

### SCENARIO 1: Plateau is created with valid dimensions

**Scenario ID**: PLATEAU-STORY-001-S1

**GIVEN**
* Upper-right corner coordinates `5 5` are provided

**WHEN**
* A `Plateau` is constructed

**THEN**
* The grid spans `(0,0)` to `(5,5)` inclusive
* `is_within(0, 0)` returns `True`
* `is_within(5, 5)` returns `True`

---

### SCENARIO 2: Point inside bounds is accepted

**Scenario ID**: PLATEAU-STORY-001-S2

**GIVEN**
* A `Plateau(5, 5)` exists

**WHEN**
* `is_within(3, 2)` is called

**THEN**
* Returns `True`

---

### SCENARIO 3: Point outside bounds is rejected

**Scenario ID**: PLATEAU-STORY-001-S3

**GIVEN**
* A `Plateau(5, 5)` exists

**WHEN**
* `is_within(6, 0)` or `is_within(-1, 3)` is called

**THEN**
* Returns `False`

---

### SCENARIO 4: Plateau is immutable after construction

**Scenario ID**: PLATEAU-STORY-001-S4

**GIVEN**
* A `Plateau(5, 5)` has been created

**WHEN**
* Any attempt is made to modify `width` or `height`

**THEN**
* An exception is raised and dimensions remain unchanged

---

## Backend Sub-Story

**Story ID**: PLATEAU-BE-001.1

**As a** developer **I want** an immutable `Plateau` value object **so that** boundary checks are reliable and side-effect-free.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `Plateau`; [08-cross-cutting-concepts.md](../../architecture/08-cross-cutting-concepts.md) — immutability

**Scenarios:**

### SCENARIO 1: Domain model enforces immutability

**Scenario ID**: PLATEAU-BE-001.1-S1

**GIVEN**
* `Plateau` is implemented as a frozen dataclass

**WHEN**
* A test attempts `plateau.width = 10`

**THEN**
* A `FrozenInstanceError` (or equivalent) is raised

---

### Domain model — `mars_rover/domain/plateau.py`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Plateau:
    """Immutable rectangular grid. Lower-left is always (0, 0)."""

    width: int
    height: int

    def is_within(self, x: int, y: int) -> bool:
        return 0 <= x <= self.width and 0 <= y <= self.height
```

**Design notes:**
- `frozen=True` enforces immutability (PLATEAU-STORY-001-S4, cross-cutting concept from `08-cross-cutting-concepts.md`)
- No I/O, no framework imports — pure domain object (TC-2)
- `is_within` is the single boundary-check entry point used by `MoveForward` (see NAV-STORY-001)

### Unit tests — `tests/domain/test_plateau.py`

```python
import pytest
from mars_rover.domain.plateau import Plateau


def test_plateau_contains_origin():
    assert Plateau(5, 5).is_within(0, 0) is True


def test_plateau_contains_upper_right_corner():
    assert Plateau(5, 5).is_within(5, 5) is True


def test_plateau_contains_interior_point():
    assert Plateau(5, 5).is_within(3, 2) is True


def test_plateau_rejects_x_too_large():
    assert Plateau(5, 5).is_within(6, 0) is False


def test_plateau_rejects_y_too_large():
    assert Plateau(5, 5).is_within(0, 6) is False


def test_plateau_rejects_negative_x():
    assert Plateau(5, 5).is_within(-1, 3) is False


def test_plateau_rejects_negative_y():
    assert Plateau(5, 5).is_within(3, -1) is False


def test_plateau_is_immutable():
    plateau = Plateau(5, 5)
    with pytest.raises(Exception):
        plateau.width = 10  # type: ignore[misc]
```

---

## Frontend Sub-Story

**Story ID**: PLATEAU-FE-001.1

**As an** operator **I want** to specify the plateau via plain-text stdin **so that** I can define the mission grid without a GUI.

**Architecture Reference**: [03-context.md](../../architecture/03-context.md) — Operator → System interface; [07-deployment.md](../../architecture/07-deployment.md) — single-process CLI

**Scenarios:**

### SCENARIO 1: Plateau line is the first line of stdin

**Scenario ID**: PLATEAU-FE-001.1-S1

**GIVEN**
* The operator pipes a text file to the CLI

**WHEN**
* The first line is `5 5`

**THEN**
* The system creates a `Plateau(5, 5)` and proceeds to parse rover blocks

No browser or GUI component required. The plateau is defined via stdin text (see CLI-STORY-001 — CLI pipe input).

---

## Infrastructure Sub-Story

**Story ID**: PLATEAU-INFRA-001.1

**As a** developer **I want** the plateau configuration to be stored in a DynamoDB table **so that** mission definitions persist across Lambda invocations and operators do not need to re-specify the grid on every request.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [09-architecture-decisions.md](../../architecture/09-architecture-decisions.md) — ADR-001 DynamoDB single-table design; [02-constraints.md](../../architecture/02-constraints.md) — TC-1

---

### SCENARIO 1: Plateau record is written to DynamoDB on mission creation

**Scenario ID**: PLATEAU-INFRA-001.1-S1

**GIVEN**
* A DynamoDB table `MarsRoverMissions` exists with `PK` (partition key) and `SK` (sort key)
* A new mission is submitted with plateau `5 5`

**WHEN**
* The `CreateMission` Lambda handler is invoked

**THEN**
* A record is written with `PK=MISSION#<id>`, `SK=PLATEAU`, `width=5`, `height=5`
* The write succeeds with HTTP 201
* The mission ID is returned to the caller

**DynamoDB item shape:**
```json
{
  "PK": "MISSION#abc123",
  "SK": "PLATEAU",
  "width": 5,
  "height": 5,
  "createdAt": "2026-04-17T10:00:00Z"
}
```

---

### SCENARIO 2: Plateau record is read back before command execution

**Scenario ID**: PLATEAU-INFRA-001.1-S2

**GIVEN**
* A plateau record exists in DynamoDB for mission `abc123`

**WHEN**
* The `ExecuteCommands` Lambda handler is invoked with `missionId=abc123`

**THEN**
* The handler reads `PK=MISSION#abc123`, `SK=PLATEAU` from DynamoDB
* A `Plateau(width, height)` domain object is reconstructed in memory
* No plateau dimensions are passed in the request body

---

### SCENARIO 3: Lambda function is deployed via AWS SAM or CDK

**Scenario ID**: PLATEAU-INFRA-001.1-S3

**GIVEN**
* An `template.yaml` (SAM) or CDK stack defines the `CreateMission` Lambda

**WHEN**
* `sam deploy` or `cdk deploy` is run locally

**THEN**
* The Lambda function is created in the target AWS account
* The function has an IAM role with `dynamodb:PutItem` permission on `MarsRoverMissions`
* The function environment variable `TABLE_NAME` is set to the DynamoDB table name

**SAM resource snippet:**
```yaml
CreateMissionFunction:
  Type: AWS::Serverless::Function
  Properties:
    Handler: mars_rover.handlers.create_mission.handler
    Runtime: python3.12
    Environment:
      Variables:
        TABLE_NAME: !Ref MarsRoverMissionsTable
    Policies:
      - Statement:
          - Effect: Allow
            Action:
              - dynamodb:PutItem
              - dynamodb:GetItem
            Resource: !GetAtt MarsRoverMissionsTable.Arn
          - Effect: Allow
            Action:
              - events:PutEvents
            Resource: !GetAtt MarsRoverEventBus.Arn
```

---

### SCENARIO 4: CloudWatch alarm fires when plateau writes fail

**Scenario ID**: PLATEAU-INFRA-001.1-S4

**GIVEN**
* A CloudWatch alarm is configured on the `CreateMission` Lambda's error metric

**WHEN**
* The Lambda function throws an unhandled exception (e.g. DynamoDB throttle)

**THEN**
* The `CreateMissionErrors` CloudWatch alarm transitions to `ALARM` state within 1 minute
* An SNS notification is sent to the ops team
* The error is logged to CloudWatch Logs with the mission ID and exception message

**CloudWatch alarm (SAM):**
```yaml
CreateMissionErrorAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: CreateMission-Errors
    MetricName: Errors
    Namespace: AWS/Lambda
    Dimensions:
      - Name: FunctionName
        Value: !Ref CreateMissionFunction
    Statistic: Sum
    Period: 60
    EvaluationPeriods: 1
    Threshold: 1
    ComparisonOperator: GreaterThanOrEqualToThreshold
    AlarmActions:
      - !Ref OpsAlertTopic
```

---

## Definition of Done

- [ ] `Plateau` dataclass implemented in `mars_rover/domain/plateau.py`
- [ ] All 8 unit tests pass (`pytest tests/domain/test_plateau.py`)
- [ ] DynamoDB table `MarsRoverMissions` defined in `template.yaml` with `PK` and `SK`
- [ ] `CreateMission` Lambda writes plateau record with correct item shape
- [ ] `ExecuteCommands` Lambda reads plateau record and reconstructs `Plateau` domain object
- [ ] Lambda IAM role has `dynamodb:PutItem` and `dynamodb:GetItem` on the table
- [ ] `CreateMissionErrors` CloudWatch alarm defined; fires on Lambda error
- [ ] `ruff`, `black`, and `isort` pass with no warnings
- [ ] No imports from `adapters/` or `application/` inside `domain/`
