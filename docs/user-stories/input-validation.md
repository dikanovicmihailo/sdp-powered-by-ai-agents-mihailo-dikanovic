# STORY-008 — Input Validation & Errors

## Story

> As an **operator**,
> I want to receive a clear error message on stderr when my input is malformed,
> so that I can identify and fix the problem quickly.

---

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC-1 | Plateau line `5` (missing height) | CLI runs | Stderr: `Input error: Plateau line must be 'WIDTH HEIGHT'…`; exit code 1 |
| AC-2 | Rover line `1 2 X` (invalid heading) | CLI runs | Stderr: `Input error: Invalid heading 'X'…`; exit code 1 |
| AC-3 | Rover line `a b N` (non-integer coords) | CLI runs | Stderr: `Input error: Rover coordinates must be integers…`; exit code 1 |
| AC-4 | Valid input | CLI runs | Nothing written to stderr; exit code 0 |
| AC-5 | Any error | CLI runs | stdout is empty (error does not pollute the result stream) |

---

## Architecture References

- **R-2** — risk: input format ambiguity; `InputParser` raises `ValueError` with descriptive message
- **08-cross-cutting-concepts.md** — malformed input raises `ValueError` in `InputParser`; propagates to `__main__` which prints to stderr and exits with code 1
- **TD-4** — technical debt: positional/fragile parser; this story partially addresses it with per-field error messages

---

## Backend

Validation logic lives in `InputParser` (STORY-007). This story adds integration-level tests that verify the full CLI error path.

No new production code is required beyond what STORY-007 already specifies.

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

## Frontend

Error messages appear on the terminal's stderr stream. The operator sees them inline when running the CLI:

```
$ printf '5\n1 2 N\nM\n' | python -m mars_rover
Input error: Plateau line must be 'WIDTH HEIGHT', got: '5'
$ echo $?
1
```

No UI component required.

---

## Infrastructure

No infrastructure changes. Error handling is entirely within the CLI process.

---

## Definition of Done

- [ ] All 8 CLI error integration tests pass
- [ ] Exit code is 1 on any `ValueError` from `InputParser`
- [ ] Error message is written to stderr, not stdout
- [ ] stdout is empty when an error occurs
- [ ] `ruff`, `black`, and `isort` pass with no warnings
