# CLI-STORY-001 — CLI Pipe Input

## Story

> As an **operator**,
> I want to pipe a plain-text input file to the CLI,
> so that I can run a full mission without typing commands interactively.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `InputParser`, `__main__` adapter; [01-introduction.md](../../architecture/01-introduction.md) — FR-1, FR-2, FR-3; [02-constraints.md](../../architecture/02-constraints.md) — TC-3

---

## Scenarios

### SCENARIO 1: Valid input is parsed into plateau and rover pairs

**Scenario ID**: CLI-STORY-001-S1

**GIVEN**
* Valid input text with plateau + 2 rovers is provided

**WHEN**
* `InputParser.parse()` is called

**THEN**
* Returns a `Plateau` and a list of `(Rover, command_string)` pairs

---

### SCENARIO 2: Kata example input is parsed correctly

**Scenario ID**: CLI-STORY-001-S2

**GIVEN**
* Input `5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM`

**WHEN**
* `InputParser.parse()` is called

**THEN**
* Returns `Plateau(5,5)`, `Rover(1,2,N)+"LMLMLMLMM"`, `Rover(3,3,E)+"MMRMMRMRRM"`

---

### SCENARIO 3: CLI accepts piped input end-to-end

**Scenario ID**: CLI-STORY-001-S3

**GIVEN**
* A valid input file exists

**WHEN**
* The CLI is invoked via `python -m mars_rover < input.txt`

**THEN**
* Correct output is printed to stdout

---

### SCENARIO 4: Single rover input is parsed correctly

**Scenario ID**: CLI-STORY-001-S4

**GIVEN**
* Input contains a plateau and one rover block

**WHEN**
* `InputParser.parse()` is called

**THEN**
* Returns one `(Rover, command_string)` pair

---

## Backend Sub-Story

**Story ID**: CLI-BE-001.1

**As a** developer **I want** an `InputParser` that converts raw stdin text into domain objects **so that** the domain layer never handles raw strings.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `InputParser`; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — Hexagonal architecture (adapter layer); [11-risks-and-technical-debts.md](../../architecture/11-risks-and-technical-debts.md) — TD-4

**Scenarios:**

### SCENARIO 1: Parser raises ValueError with descriptive message on bad plateau line

**Scenario ID**: CLI-BE-001.1-S1

**GIVEN**
* Input plateau line is `5` (missing height)

**WHEN**
* `InputParser.parse()` is called

**THEN**
* A `ValueError` is raised with a message containing `"Plateau"`

---

### SCENARIO 2: Parser raises ValueError on invalid heading

**Scenario ID**: CLI-BE-001.1-S2

**GIVEN**
* Rover line is `1 2 X`

**WHEN**
* `InputParser.parse()` is called

**THEN**
* A `ValueError` is raised with a message containing `"heading"`

---

### Adapter — `mars_rover/adapters/input_parser.py`

```python
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


class InputParser:
    def parse(self, text: str) -> tuple[Plateau, list[tuple[Rover, str]]]:
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

        plateau = self._parse_plateau(lines[0])

        missions: list[tuple[Rover, str]] = []
        for i in range(1, len(lines), 2):
            rover = self._parse_rover(lines[i])
            command_string = lines[i + 1]
            missions.append((rover, command_string))

        return plateau, missions

    def _parse_plateau(self, line: str) -> Plateau:
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Plateau line must be 'WIDTH HEIGHT', got: {line!r}")
        try:
            width, height = int(parts[0]), int(parts[1])
        except ValueError:
            raise ValueError(f"Plateau dimensions must be integers, got: {line!r}")
        if width < 0 or height < 0:
            raise ValueError(f"Plateau dimensions must be non-negative, got: {line!r}")
        return Plateau(width, height)

    def _parse_rover(self, line: str) -> Rover:
        parts = line.split()
        if len(parts) != 3:
            raise ValueError(f"Rover line must be 'X Y HEADING', got: {line!r}")
        try:
            x, y = int(parts[0]), int(parts[1])
        except ValueError:
            raise ValueError(f"Rover coordinates must be integers, got: {line!r}")
        try:
            heading = Heading(parts[2])
        except ValueError:
            raise ValueError(
                f"Invalid heading {parts[2]!r}. Must be one of N, E, S, W."
            )
        return Rover(x, y, heading)
```

### Entry point — `mars_rover/__main__.py`

```python
import sys
from mars_rover.adapters.input_parser import InputParser
from mars_rover.adapters.output_formatter import OutputFormatter
from mars_rover.application.mission_controller import MissionController


def main() -> None:
    text = sys.stdin.read()
    try:
        parser = InputParser()
        plateau, missions = parser.parse(text)
    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        sys.exit(1)

    controller = MissionController(plateau)
    rovers = controller.run(missions)

    formatter = OutputFormatter()
    for rover in rovers:
        print(formatter.format(rover))


if __name__ == "__main__":
    main()
```

> **Note:** This entry point is the initial implementation. NAV-STORY-003 (obstacle detection) updates `MissionController.run()` to return `list[tuple[Rover, bool]]` and updates this loop accordingly — see `obstacle-detection.md`.

### Unit tests — `tests/adapters/test_input_parser.py`

```python
import pytest
from mars_rover.adapters.input_parser import InputParser
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau


KATA_INPUT = "5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM\n"


def test_parse_plateau():
    parser = InputParser()
    plateau, _ = parser.parse(KATA_INPUT)
    assert plateau == Plateau(5, 5)


def test_parse_two_rovers():
    parser = InputParser()
    _, missions = parser.parse(KATA_INPUT)
    assert len(missions) == 2


def test_parse_rover_1_position():
    parser = InputParser()
    _, missions = parser.parse(KATA_INPUT)
    rover, cmd = missions[0]
    assert rover.x == 1 and rover.y == 2 and rover.heading == Heading.N
    assert cmd == "LMLMLMLMM"


def test_parse_rover_2_position():
    parser = InputParser()
    _, missions = parser.parse(KATA_INPUT)
    rover, cmd = missions[1]
    assert rover.x == 3 and rover.y == 3 and rover.heading == Heading.E
    assert cmd == "MMRMMRMRRM"


def test_parse_invalid_plateau_raises():
    with pytest.raises(ValueError, match="Plateau"):
        InputParser().parse("5\n1 2 N\nM\n")


def test_parse_invalid_heading_raises():
    with pytest.raises(ValueError, match="heading"):
        InputParser().parse("5 5\n1 2 X\nM\n")


def test_parse_non_integer_coordinates_raises():
    with pytest.raises(ValueError, match="integers"):
        InputParser().parse("5 5\na b N\nM\n")
```

---

## Frontend Sub-Story

**Story ID**: CLI-FE-001.1

**As an** operator **I want** to pipe a text file to the CLI **so that** I can run missions non-interactively from scripts or CI.

**Architecture Reference**: [03-context.md](../../architecture/03-context.md) — Operator → System interface; [07-deployment.md](../../architecture/07-deployment.md) — single-process CLI

**Scenarios:**

### SCENARIO 1: Operator pipes a file to the CLI

**Scenario ID**: CLI-FE-001.1-S1

**GIVEN**
* A valid input file `input.txt` exists

**WHEN**
* The operator runs `python -m mars_rover < input.txt`

**THEN**
* The CLI reads from stdin, processes the mission, and prints results to stdout

```bash
# Pipe a file
python -m mars_rover < input.txt

# Inline heredoc
python -m mars_rover <<EOF
5 5
1 2 N
LMLMLMLMM
EOF
```

---

## Infrastructure Sub-Story

**Story ID**: CLI-INFRA-001.1

**As a** developer **I want** the `CreateMission` Lambda to be the entry point for submitting mission input **so that** operators interact with the system via an API Gateway endpoint rather than a CLI pipe.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [09-architecture-decisions.md](../../architecture/09-architecture-decisions.md) — ADR-001; [02-constraints.md](../../architecture/02-constraints.md) — TC-1, TC-3

---

### SCENARIO 1: POST /missions creates a mission record and returns a mission ID

**Scenario ID**: CLI-INFRA-001.1-S1

**GIVEN**
* An API Gateway `POST /missions` route targets the `CreateMission` Lambda
* This is the same `CreateMission` Lambda introduced in PLATEAU-INFRA-001.1; this story covers its full API contract

**WHEN**
* An operator sends:
  ```http
  POST /missions
  Content-Type: application/json

  {
    "plateau": { "width": 5, "height": 5 },
    "rovers": [
      { "x": 1, "y": 2, "heading": "N", "commands": "LMLMLMLMM" },
      { "x": 3, "y": 3, "heading": "E", "commands": "MMRMMRMRRM" }
    ]
  }
  ```

**THEN**
* The Lambda writes a plateau record (`SK=PLATEAU`), a metadata record (`SK=METADATA` with `roverCount=2`), and one rover record per rover (`SK=ROVER#0`, `SK=ROVER#1`) to DynamoDB — all with `commands` stored on each rover record
* Returns HTTP 201 with `{ "missionId": "<uuid>" }`
* Publishes a `MissionCreated` event to `MarsRoverEventBus`

---

### SCENARIO 2: CreateMission Lambda validates input and returns 400 on bad data

**Scenario ID**: CLI-INFRA-001.1-S2

**GIVEN**
* The `CreateMission` Lambda uses `InputParser` to validate the request body

**WHEN**
* An operator sends a rover with `"heading": "X"` (invalid)

**THEN**
* The Lambda returns HTTP 400 with `{ "error": "Invalid heading 'X'. Must be one of N, E, S, W." }`
* No DynamoDB writes occur
* No event is published
* The error is logged to CloudWatch Logs at `WARN` level

---

### SCENARIO 3: Lambda is deployed with API Gateway via SAM

**Scenario ID**: CLI-INFRA-001.1-S3

**GIVEN**
* `template.yaml` defines the `CreateMission` Lambda with an API Gateway event

**WHEN**
* `sam deploy` is run

**THEN**
* The Lambda is deployed with `POST /missions` route on the API Gateway
* The Lambda has `dynamodb:PutItem` on `MarsRoverMissions` and `events:PutEvents` on `MarsRoverEventBus`
* The API Gateway URL is printed as a CloudFormation output

**SAM resource snippet:**
```yaml
CreateMissionFunction:
  Type: AWS::Serverless::Function
  Properties:
    Handler: mars_rover.handlers.create_mission.handler
    Runtime: python3.12
    Events:
      CreateMission:
        Type: Api
        Properties:
          Path: /missions
          Method: POST
    Policies:
      - Statement:
          - Effect: Allow
            Action:
              - dynamodb:PutItem
            Resource: !GetAtt MarsRoverMissionsTable.Arn
          - Effect: Allow
            Action:
              - events:PutEvents
            Resource: !GetAtt MarsRoverEventBus.Arn
```

---

### SCENARIO 4: CloudWatch alarm fires when CreateMission error rate exceeds 1%

**Scenario ID**: CLI-INFRA-001.1-S4

**GIVEN**
* A CloudWatch alarm monitors the `CreateMission` Lambda error rate

**WHEN**
* More than 1% of invocations in a 5-minute window result in errors

**THEN**
* The `CreateMissionHighErrorRate` alarm transitions to `ALARM`
* The alarm uses the `Errors / Invocations` metric math expression
* An SNS notification is sent to the ops team

---

## Definition of Done

- [ ] `InputParser` implemented in `mars_rover/adapters/input_parser.py`
- [ ] All parser unit tests pass
- [ ] `CreateMission` Lambda writes plateau + rover records to DynamoDB and returns `missionId`
- [ ] Lambda returns HTTP 400 with descriptive message on invalid input (no DynamoDB write)
- [ ] `POST /missions` API Gateway route defined in `template.yaml`
- [ ] `MissionCreated` event published to `MarsRoverEventBus` on success
- [ ] `CreateMissionHighErrorRate` CloudWatch alarm defined; fires when error rate > 1%
- [ ] `ruff`, `black`, and `isort` pass with no warnings
