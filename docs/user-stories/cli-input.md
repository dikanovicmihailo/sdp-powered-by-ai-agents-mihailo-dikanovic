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

**As a** developer **I want** the CLI input parsing functionality to be containerized and testable **so that** input validation works consistently across environments.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [02-constraints.md](../../architecture/02-constraints.md) — TC-1, TC-3

---

### SCENARIO 1: Container processes stdin input and validates format

**Scenario ID**: CLI-INFRA-001.1-S1

**GIVEN**
* The Docker container is built with the CLI input parser
* A valid input file exists with plateau and rover data

**WHEN**
* `echo "5 5\n1 2 N\nLMLMLMLMM" | docker run -i --rm mars-rover` is executed

**THEN**
* The container reads from stdin successfully
* Input parsing validates the plateau dimensions and rover position
* The container processes the input without errors
* Output is written to stdout

---

### SCENARIO 2: Container validates input and logs errors to stderr

**Scenario ID**: CLI-INFRA-001.1-S2

**GIVEN**
* The Docker container includes input validation logic
* Invalid input with bad heading is provided

**WHEN**
* `echo "5 5\n1 2 X\nM" | docker run -i --rm mars-rover` is executed

**THEN**
* The container detects the invalid heading "X"
* Error message is logged to stderr with descriptive text
* Container exits with non-zero exit code
* No processing of invalid data occurs

---

### SCENARIO 3: Dockerfile builds with input parsing dependencies

**Scenario ID**: CLI-INFRA-001.1-S3

**GIVEN**
* The `requirements.txt` includes all necessary parsing dependencies
* The Dockerfile copies the input parser code

**WHEN**
* `docker build -t mars-rover .` is executed

**THEN**
* The build includes `mars_rover/adapters/input_parser.py`
* All dependencies for input validation are installed
* The container can import and use the InputParser class
* Build completes without dependency errors

---

### SCENARIO 4: Test suite validates input parsing inside container

**Scenario ID**: CLI-INFRA-001.1-S4

**GIVEN**
* Test files exist for input parser functionality
* The Docker container includes pytest

**WHEN**
* `docker run --rm mars-rover pytest tests/adapters/test_input_parser.py -v` is executed

**THEN**
* All input parser tests run inside the container
* Tests validate plateau parsing, rover parsing, and error handling
* pytest discovers and executes all parser-related tests
* Container exits with code 0 on test success

---

## Definition of Done

- [ ] `InputParser` implemented in `mars_rover/adapters/input_parser.py`
- [ ] All parser unit tests pass
- [ ] Container processes stdin input and validates format correctly
- [ ] Container logs validation errors to stderr with descriptive messages
- [ ] Dockerfile builds successfully with input parsing dependencies
- [ ] Test suite runs inside container and validates input parsing
- [ ] `ruff`, `black`, and `isort` pass with no warnings
