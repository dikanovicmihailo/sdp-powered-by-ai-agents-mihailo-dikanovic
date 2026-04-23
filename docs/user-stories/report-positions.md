# CLI-STORY-002 — Report Final Positions

## Story

> As an **operator**,
> I want to receive the final position and heading of every rover after all commands have run,
> so that I know where each rover ended up.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `OutputFormatter` adapter; [01-introduction.md](../../architecture/01-introduction.md) — FR-5; [03-context.md](../../architecture/03-context.md) — System → Operator interface (stdout)

---

## Scenarios

### SCENARIO 1: Single rover output is formatted correctly

**Scenario ID**: CLI-STORY-002-S1

**GIVEN**
* A rover ends at `x=1, y=3, heading=N`

**WHEN**
* `OutputFormatter.format(rover)` is called

**THEN**
* The returned string is `1 3 N`

---

### SCENARIO 2: Multiple rovers produce one line each in order

**Scenario ID**: CLI-STORY-002-S2

**GIVEN**
* Two rovers complete their missions in deployment order

**WHEN**
* Output is produced

**THEN**
* Two lines are printed to stdout, one per rover, in deployment order

---

### SCENARIO 3: Output goes to stdout, not stderr

**Scenario ID**: CLI-STORY-002-S3

**GIVEN**
* A valid mission completes

**WHEN**
* The CLI writes output

**THEN**
* All rover position lines appear on stdout
* stderr is empty

---

## Backend Sub-Story

**Story ID**: CLI-BE-002.1

**As a** developer **I want** a thin `OutputFormatter` adapter **so that** rover state serialisation is isolated from domain logic and easily testable.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `OutputFormatter`; [04-solution-strategy.md](../../architecture/04-solution-strategy.md) — Hexagonal architecture (adapter layer)

**Scenarios:**

### SCENARIO 1: Formatter returns space-separated string

**Scenario ID**: CLI-BE-002.1-S1

**GIVEN**
* A `Rover(5, 1, Heading.E)` exists

**WHEN**
* `OutputFormatter().format(rover)` is called

**THEN**
* Returns `"5 1 E"`

---

### Adapter — `mars_rover/adapters/output_formatter.py`

```python
from mars_rover.domain.rover import Rover


class OutputFormatter:
    def format(self, rover: Rover) -> str:
        return f"{rover.x} {rover.y} {rover.heading.value}"
```

**Design notes:**
- Thin adapter — only responsibility is serialising `Rover` state to the wire format
- Returns a `str` rather than printing directly, keeping it testable with plain strings (no stdout capture needed)
- `heading.value` extracts the string representation from the `Heading` enum (`"N"`, `"E"`, etc.)

### Unit tests — `tests/adapters/test_output_formatter.py`

```python
from mars_rover.adapters.output_formatter import OutputFormatter
from mars_rover.domain.heading import Heading
from mars_rover.domain.rover import Rover


def test_format_kata_example_1():
    rover = Rover(1, 3, Heading.N)
    assert OutputFormatter().format(rover) == "1 3 N"


def test_format_kata_example_2():
    rover = Rover(5, 1, Heading.E)
    assert OutputFormatter().format(rover) == "5 1 E"


def test_format_origin_facing_south():
    rover = Rover(0, 0, Heading.S)
    assert OutputFormatter().format(rover) == "0 0 S"


def test_format_all_headings():
    formatter = OutputFormatter()
    cases = [
        (Heading.N, "0 0 N"),
        (Heading.E, "0 0 E"),
        (Heading.S, "0 0 S"),
        (Heading.W, "0 0 W"),
    ]
    for heading, expected in cases:
        assert formatter.format(Rover(0, 0, heading)) == expected
```

---

## Frontend Sub-Story

**Story ID**: CLI-FE-002.1

**As an** operator **I want** to read rover positions from stdout **so that** I can capture or redirect the output in shell scripts.

**Architecture Reference**: [03-context.md](../../architecture/03-context.md) — System → Operator interface; [07-deployment.md](../../architecture/07-deployment.md) — single-process CLI

**Scenarios:**

### SCENARIO 1: Output is readable from terminal or shell redirection

**Scenario ID**: CLI-FE-002.1-S1

**GIVEN**
* A mission completes successfully

**WHEN**
* The operator reads stdout

**THEN**
* Each line contains `x y HEADING` for one rover
* The output can be captured with `> output.txt` or piped to another command

The output is plain text on stdout — one line per rover. No UI component required.

---

## Infrastructure Sub-Story

**Story ID**: CLI-INFRA-002.1

**As a** developer **I want** the output formatting functionality to be containerized and testable **so that** rover position reporting works consistently across environments.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [01-introduction.md](../../architecture/01-introduction.md) — FR-5

---

### SCENARIO 1: Container formats and outputs rover positions correctly

**Scenario ID**: CLI-INFRA-002.1-S1

**GIVEN**
* The Docker container includes output formatting logic
* Multiple rovers have completed their missions with final positions

**WHEN**
* The container processes the mission results

**THEN**
* Each rover position is formatted as "x y HEADING"
* Rovers are output in deployment order
* Output is written to stdout with proper line endings

---

### SCENARIO 2: Container handles missing or invalid rover data gracefully

**Scenario ID**: CLI-INFRA-002.1-S2

**GIVEN**
* The Docker container includes error handling for output formatting
* Some rover data is missing or corrupted

**WHEN**
* The container attempts to format the output

**THEN**
* Error is logged to stderr with descriptive message
* Container exits with non-zero exit code
* No partial or invalid output is produced

---

### SCENARIO 3: Dockerfile builds with output formatting dependencies

**Scenario ID**: CLI-INFRA-002.1-S3

**GIVEN**
* The `mars_rover/adapters/output_formatter.py` file exists
* The Dockerfile includes adapter layer code

**WHEN**
* `docker build -t mars-rover .` is executed

**THEN**
* The build includes output formatting code at `/app/mars_rover/adapters/output_formatter.py`
* All formatting-related dependencies are available
* The container can import and use the OutputFormatter class
* Build completes without errors

---

### SCENARIO 4: Test suite validates output formatting inside container

**Scenario ID**: CLI-INFRA-002.1-S4

**GIVEN**
* Test files exist for output formatting functionality
* The Docker container includes pytest

**WHEN**
* `docker run --rm mars-rover pytest tests/adapters/test_output_formatter.py -v` is executed

**THEN**
* All output formatting tests run inside the container
* Tests validate correct position formatting and error handling
* pytest discovers and executes all formatter-related tests
* Container exits with code 0 on test success

---

## Definition of Done

- [ ] `OutputFormatter` implemented in `mars_rover/adapters/output_formatter.py`
- [ ] All formatter unit tests pass
- [ ] Container formats and outputs rover positions correctly
- [ ] Container handles missing or invalid rover data gracefully
- [ ] Dockerfile builds successfully with output formatting dependencies
- [ ] Test suite runs inside container and validates output formatting
- [ ] `ruff`, `black`, and `isort` pass with no warnings
