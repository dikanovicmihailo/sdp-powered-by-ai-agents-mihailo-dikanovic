# STORY-004 — Report Final Positions

## Story

> As an **operator**,
> I want to receive the final position and heading of every rover after all commands have run,
> so that I know where each rover ended up.

---

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC-1 | Rover ends at `x=1, y=3, heading=N` | Output is formatted | Line reads `1 3 N` |
| AC-2 | Rover ends at `x=5, y=1, heading=E` | Output is formatted | Line reads `5 1 E` |
| AC-3 | Two rovers complete their missions | Output is produced | One line per rover, in deployment order |
| AC-4 | Output is written | Channel used | Written to stdout, not stderr |

---

## Architecture References

- **FR-5** — system reports final position and heading of every rover
- **QS-1 / QS-2** — correctness scenarios require exact output match
- Component: `adapters/output_formatter.py` → `OutputFormatter`
- Interface: System → Operator (stdout) from `03-context.md`

---

## Backend

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

## Frontend

The output is plain text on stdout — one line per rover:

```
1 3 N
5 1 E
```

No UI component required. The operator reads this directly from the terminal or captures it via shell redirection.

---

## Infrastructure

No infrastructure changes. Output goes to stdout of the single CLI process (see `07-deployment.md`).

---

## Definition of Done

- [ ] `OutputFormatter` implemented in `mars_rover/adapters/output_formatter.py`
- [ ] All formatter unit tests pass
- [ ] Output matches kata expected format exactly (space-separated `x y HEADING`)
- [ ] `ruff`, `black`, and `isort` pass with no warnings
