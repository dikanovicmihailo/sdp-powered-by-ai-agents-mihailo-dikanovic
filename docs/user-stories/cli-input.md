# STORY-007 — CLI Pipe Input

## Story

> As an **operator**,
> I want to pipe a plain-text input file to the CLI,
> so that I can run a full mission without typing commands interactively.

---

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC-1 | Valid input text with plateau + 2 rovers | `InputParser.parse()` is called | Returns a `Plateau` and a list of `(Rover, command_string)` pairs |
| AC-2 | Input `5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM` | Parsed | `Plateau(5,5)`, `Rover(1,2,N)+"LMLMLMLMM"`, `Rover(3,3,E)+"MMRMMRMRRM"` |
| AC-3 | Valid input | CLI invoked via `python -m mars_rover < input.txt` | Correct output printed to stdout |
| AC-4 | Input with a single rover | Parsed | Returns one `(Rover, command_string)` pair |

---

## Architecture References

- **FR-1 / FR-2 / FR-3** — plateau, rover position, and command string all come from stdin
- **TC-3** — input/output via stdin/stdout
- **TD-4** — risk: positional/fragile parser; clear error messages per field
- Components: `adapters/input_parser.py` → `InputParser`, `__main__.py` → entry point

---

## Backend

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

## Frontend

The operator interacts via the shell:

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

No browser or GUI component required.

---

## Infrastructure

No infrastructure changes. The CLI reads from stdin and writes to stdout within the single Python process (see `07-deployment.md`).

**Development setup reminder:**

```bash
pip install -e ".[dev]"
pytest
```

---

## Definition of Done

- [ ] `InputParser` implemented in `mars_rover/adapters/input_parser.py`
- [ ] `__main__.py` entry point wires parser → controller → formatter
- [ ] All parser unit tests pass
- [ ] `python -m mars_rover < input.txt` produces correct output end-to-end
- [ ] Malformed input exits with code 1 and prints to stderr (covered in STORY-008)
- [ ] `ruff`, `black`, and `isort` pass with no warnings
