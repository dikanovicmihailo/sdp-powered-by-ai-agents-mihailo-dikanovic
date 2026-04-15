# CLI-STORY-003 — Input Validation & Errors

## Story

> As an **operator**,
> I want to receive a clear error message on stderr when my input is malformed,
> so that I can identify and fix the problem quickly.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `InputParser`; [08-cross-cutting-concepts.md](../../architecture/08-cross-cutting-concepts.md) — error handling; [11-risks-and-technical-debts.md](../../architecture/11-risks-and-technical-debts.md) — R-2, TD-4

---

## Scenarios

### SCENARIO 1: Missing plateau height produces clear error

**Scenario ID**: CLI-STORY-003-S1

**GIVEN**
* Plateau line is `5` (missing height)

**WHEN**
* The CLI runs

**THEN**
* stderr contains `Input error: Plateau line must be 'WIDTH HEIGHT'…`
* Exit code is 1

---

### SCENARIO 2: Invalid heading produces clear error

**Scenario ID**: CLI-STORY-003-S2

**GIVEN**
* Rover line is `1 2 X` (invalid heading)

**WHEN**
* The CLI runs

**THEN**
* stderr contains `Input error: Invalid heading 'X'…`
* Exit code is 1

---

### SCENARIO 3: Non-integer coordinates produce clear error

**Scenario ID**: CLI-STORY-003-S3

**GIVEN**
* Rover line is `a b N` (non-integer coords)

**WHEN**
* The CLI runs

**THEN**
* stderr contains `Input error: Rover coordinates must be integers…`
* Exit code is 1

---

### SCENARIO 4: Valid input produces no error

**Scenario ID**: CLI-STORY-003-S4

**GIVEN**
* Valid input is provided

**WHEN**
* The CLI runs

**THEN**
* Nothing is written to stderr and exit code is 0

---

### SCENARIO 5: Error does not pollute stdout

**Scenario ID**: CLI-STORY-003-S5

**GIVEN**
* Any input error occurs

**WHEN**
* The CLI runs

**THEN**
* stdout is empty (error does not pollute the result stream)

---

## Backend Sub-Story

**Story ID**: CLI-BE-003.1

**As a** developer **I want** `InputParser` to raise `ValueError` with descriptive messages **so that** the CLI can provide helpful error feedback to operators.

**Architecture Reference**: [05-building-blocks.md](../../architecture/05-building-blocks.md) — `InputParser`; [08-cross-cutting-concepts.md](../../architecture/08-cross-cutting-concepts.md) — error handling contract

**Scenarios:**

### SCENARIO 1: ValueError propagates to main with descriptive message

**Scenario ID**: CLI-BE-003.1-S1

**GIVEN**
* `InputParser.parse()` encounters malformed input

**WHEN**
* A `ValueError` is raised

**THEN**
* The exception message contains enough detail to identify the specific field and problem

Validation logic lives in `InputParser` (CLI-STORY-001). This story adds integration-level tests that verify the full CLI error path.

No new production code is required beyond what CLI-STORY-001 already specifies.

### Integration tests — `tests/test_cli_errors.py`

```python
import subprocess
import sys


def run_cli(input_text: str):
    result = subprocess.run(
        [sys.executable, "-m", "mars_rover"],
        input=input_text,
        capture_output=True,
        text=True,
    )
    return result


def test_missing_plateau_height_exits_1():
    result = run_cli("5\n1 2 N\nM\n")
    assert result.returncode == 1


def test_missing_plateau_height_stderr_message():
    result = run_cli("5\n1 2 N\nM\n")
    assert "Plateau" in result.stderr
    assert "Input error" in result.stderr


def test_invalid_heading_exits_1():
    result = run_cli("5 5\n1 2 X\nM\n")
    assert result.returncode == 1


def test_invalid_heading_stderr_message():
    result = run_cli("5 5\n1 2 X\nM\n")
    assert "heading" in result.stderr.lower()


def test_non_integer_coords_exits_1():
    result = run_cli("5 5\na b N\nM\n")
    assert result.returncode == 1


def test_valid_input_exits_0():
    result = run_cli("5 5\n1 2 N\nM\n")
    assert result.returncode == 0


def test_valid_input_empty_stderr():
    result = run_cli("5 5\n1 2 N\nM\n")
    assert result.stderr == ""


def test_error_does_not_pollute_stdout():
    result = run_cli("5 5\n1 2 X\nM\n")
    assert result.stdout == ""
```

---

## Frontend Sub-Story

**Story ID**: CLI-FE-003.1

**As an** operator **I want** error messages to appear on stderr **so that** I can distinguish errors from valid results when using shell redirection.

**Architecture Reference**: [03-context.md](../../architecture/03-context.md) — System → Operator interface; [02-constraints.md](../../architecture/02-constraints.md) — TC-3

**Scenarios:**

### SCENARIO 1: Error messages appear on stderr, not stdout

**Scenario ID**: CLI-FE-003.1-S1

**GIVEN**
* Malformed input is provided

**WHEN**
* The CLI runs

**THEN**
* Error messages appear on stderr
* stdout is empty
* The operator can redirect stdout without capturing error messages

```bash
$ printf '5\n1 2 N\nM\n' | python -m mars_rover
Input error: Plateau line must be 'WIDTH HEIGHT', got: '5'
$ echo $?
1
```

---

## Infrastructure Sub-Story

**Story ID**: CLI-INFRA-003.1

**As a** developer **I want** error handling to be entirely within the CLI process **so that** no external logging service or error tracking system is needed.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — single-process CLI, no persistence

**Scenarios:**

### SCENARIO 1: Error handling requires no external resources

**Scenario ID**: CLI-INFRA-003.1-S1

**GIVEN**
* An input error occurs

**WHEN**
* The CLI handles the error

**THEN**
* Only `sys.stderr` and `sys.exit()` are used
* No file, database, network, or logging service is contacted

No infrastructure changes. Error handling is entirely within the CLI process.

---

## Definition of Done

- [ ] All 8 CLI error integration tests pass
- [ ] Exit code is 1 on any `ValueError` from `InputParser`
- [ ] Error message is written to stderr, not stdout
- [ ] stdout is empty when an error occurs
- [ ] `ruff`, `black`, and `isort` pass with no warnings
