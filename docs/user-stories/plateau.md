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

**As a** developer **I want** the plateau functionality to be containerized and testable **so that** plateau validation and boundary checking work consistently across environments.

**Architecture Reference**: [07-deployment.md](../../architecture/07-deployment.md) — deployment topology; [02-constraints.md](../../architecture/02-constraints.md) — TC-1

---

### SCENARIO 1: Container validates plateau dimensions from input

**Scenario ID**: PLATEAU-INFRA-001.1-S1

**GIVEN**
* The Docker container includes plateau validation logic
* Input contains plateau dimensions "5 5"

**WHEN**
* The container processes the input

**THEN**
* A `Plateau(width=5, height=5)` domain object is created
* Plateau dimensions are validated as positive integers
* The plateau is available for rover boundary checking

---

### SCENARIO 2: Container logs validation errors for invalid plateau

**Scenario ID**: PLATEAU-INFRA-001.1-S2

**GIVEN**
* The Docker container includes input validation
* Invalid plateau input "-1 5" is provided

**WHEN**
* The container processes the input

**THEN**
* Validation error is logged to stderr
* Error message indicates invalid plateau dimensions
* Container exits with non-zero exit code
* No plateau object is created

---

### SCENARIO 3: Dockerfile builds with plateau domain code

**Scenario ID**: PLATEAU-INFRA-001.1-S3

**GIVEN**
* The `mars_rover/domain/plateau.py` file exists
* The Dockerfile includes domain code copying

**WHEN**
* `docker build -t mars-rover .` is executed

**THEN**
* The build includes plateau domain code at `/app/mars_rover/domain/plateau.py`
* All plateau-related dependencies are installed
* The container can import and use the Plateau class
* Build completes without errors

---

### SCENARIO 4: Test suite validates plateau functionality inside container

**Scenario ID**: PLATEAU-INFRA-001.1-S4

**GIVEN**
* Test files exist for plateau functionality in `tests/domain/test_plateau.py`
* The Docker container includes pytest

**WHEN**
* `docker run --rm mars-rover pytest tests/domain/test_plateau.py -v` is executed

**THEN**
* All 8 plateau unit tests run inside the container
* Tests validate plateau creation, boundary checking, and validation
* pytest discovers and executes all plateau-related tests
* Container exits with code 0 on test success

---

## Definition of Done

- [ ] `Plateau` dataclass implemented in `mars_rover/domain/plateau.py`
- [ ] All 8 unit tests pass (`pytest tests/domain/test_plateau.py`)
- [ ] Container validates plateau dimensions from input correctly
- [ ] Container logs validation errors for invalid plateau input
- [ ] Dockerfile builds successfully with plateau domain code
- [ ] Test suite runs inside container and validates plateau functionality
- [ ] `ruff`, `black`, and `isort` pass with no warnings
- [ ] No imports from `adapters/` or `application/` inside `domain/`
