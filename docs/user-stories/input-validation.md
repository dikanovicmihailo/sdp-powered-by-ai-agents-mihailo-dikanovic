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

**As a** developer **I want** the `CreateMission` Lambda to return structured error responses and log validation failures to CloudWatch **so that** operators get actionable error messages and the ops team can monitor input quality.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [08-cross-cutting-concepts.md](../../architecture/08-cross-cutting-concepts.md) — error handling; [11-risks-and-technical-debts.md](../../architecture/11-risks-and-technical-debts.md) — R-2, TD-3

---

### SCENARIO 1: Lambda returns HTTP 400 with structured error body on invalid input

**Scenario ID**: CLI-INFRA-003.1-S1

**GIVEN**
* The `CreateMission` Lambda receives a request with `"heading": "X"`

**WHEN**
* `InputParser.parse()` raises `ValueError`

**THEN**
* The Lambda returns HTTP 400:
  ```json
  {
    "error": "Invalid heading 'X'. Must be one of N, E, S, W.",
    "field": "rovers[0].heading"
  }
  ```
* No DynamoDB write occurs
* No event is published to EventBridge

---

### SCENARIO 2: Validation errors are logged to CloudWatch Logs at WARN level

**Scenario ID**: CLI-INFRA-003.1-S2

**GIVEN**
* The Lambda catches a `ValueError` from `InputParser`

**WHEN**
* The error response is returned

**THEN**
* A structured log line is emitted:
  ```json
  {
    "level": "WARN",
    "event": "ValidationError",
    "requestId": "<lambda-request-id>",
    "error": "Invalid heading 'X'. Must be one of N, E, S, W.",
    "field": "rovers[0].heading"
  }
  ```
* The log is queryable via CloudWatch Logs Insights using `filter event = "ValidationError"`

---

### SCENARIO 3: CloudWatch metric filter counts validation errors per minute

**Scenario ID**: CLI-INFRA-003.1-S3

**GIVEN**
* A CloudWatch metric filter is defined on the `CreateMission` log group

**WHEN**
* A `ValidationError` log event is emitted

**THEN**
* The custom metric `MarsRover/ValidationErrors` is incremented by 1
* The metric appears on the `MarsRoverOps` CloudWatch dashboard

**Metric filter (SAM):**
```yaml
ValidationErrorMetricFilter:
  Type: AWS::Logs::MetricFilter
  Properties:
    LogGroupName: !Sub "/aws/lambda/${CreateMissionFunction}"
    FilterPattern: '{ $.event = "ValidationError" }'
    MetricTransformations:
      - MetricName: ValidationErrors
        MetricNamespace: MarsRover
        MetricValue: "1"
```

---

### SCENARIO 4: CloudWatch alarm fires when validation error rate is high

**Scenario ID**: CLI-INFRA-003.1-S4

**GIVEN**
* The `MarsRover/ValidationErrors` custom metric is being published

**WHEN**
* More than 20 validation errors occur within a 5-minute window

**THEN**
* The `HighValidationErrorRate` alarm transitions to `ALARM`
* This signals a likely broken client or a change in the input format contract
* An SNS notification is sent to the ops team

---

## Definition of Done

- [ ] All 8 CLI error integration tests pass
- [ ] `CreateMission` Lambda returns HTTP 400 with `{ "error": "...", "field": "..." }` on `ValueError`
- [ ] No DynamoDB write or EventBridge event on validation failure
- [ ] Structured `ValidationError` log emitted at `WARN` level with `requestId` and `field`
- [ ] `ValidationErrorMetricFilter` defined in `template.yaml`; metric increments on each validation error
- [ ] `HighValidationErrorRate` alarm defined; fires when > 20 errors in 5 minutes
- [ ] `ruff`, `black`, and `isort` pass with no warnings
