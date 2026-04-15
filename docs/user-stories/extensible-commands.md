# STORY-010 — Extensible Command Types

## Story

> As a **developer**,
> I want to add a new command type without modifying existing domain classes,
> so that the system is open for extension and closed for modification.

---

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC-1 | New `UTurn` command (`U`) is added | `UTurn()(rover)` is called | Rover heading rotates 180° in place |
| AC-2 | `UTurn` is added | `Rover`, `Plateau`, `Heading`, `OutputFormatter` source files | Zero lines changed in any of those files |
| AC-3 | `MissionController` command map is updated with `"U": UTurn()` | Input string `U` is parsed | `UTurn` is dispatched correctly |
| AC-4 | `UTurn` is added | Existing tests | All pass without modification |

---

## Architecture References

- **QS-6** — extensibility quality scenario from `10-quality-requirements.md`
- **04-solution-strategy.md** — Command pattern: adding new commands requires no changes to existing domain logic
- **08-cross-cutting-concepts.md** — open/closed principle enforced by the Command protocol

---

## Backend

### New command — `mars_rover/domain/commands.py` (append only)

```python
class UTurn:
    """Rotate the rover 180° in place. U = two consecutive right turns."""

    def __call__(self, rover: "Rover") -> None:
        rover.heading = rover.heading.turn_right().turn_right()
```

### Command map update — `mars_rover/application/mission_controller.py`

The only change outside `commands.py` is registering the new letter in the command map inside `MissionController`:

```python
# In MissionController.__init__ or wherever the map lives:
command_map = {
    "L": TurnLeft(),
    "R": TurnRight(),
    "M": MoveForward(self._plateau),
    "U": UTurn(),          # ← only addition required
}
```

### Unit tests — `tests/domain/test_extensible_commands.py`

```python
from mars_rover.domain.commands import UTurn
from mars_rover.domain.heading import Heading
from mars_rover.domain.rover import Rover


def test_uturn_from_north():
    rover = Rover(0, 0, Heading.N)
    UTurn()(rover)
    assert rover.heading == Heading.S


def test_uturn_from_east():
    rover = Rover(0, 0, Heading.E)
    UTurn()(rover)
    assert rover.heading == Heading.W


def test_uturn_from_south():
    rover = Rover(0, 0, Heading.S)
    UTurn()(rover)
    assert rover.heading == Heading.N


def test_uturn_from_west():
    rover = Rover(0, 0, Heading.W)
    UTurn()(rover)
    assert rover.heading == Heading.E


def test_uturn_does_not_move():
    rover = Rover(3, 4, Heading.N)
    UTurn()(rover)
    assert rover.x == 3 and rover.y == 4


def test_uturn_via_rover_execute():
    rover = Rover(0, 0, Heading.N)
    rover.execute(UTurn())
    assert rover.heading == Heading.S
```

### Proof of open/closed compliance

Files touched to add `UTurn`:

| File | Change |
|------|--------|
| `mars_rover/domain/commands.py` | Add `UTurn` class (new code only) |
| `mars_rover/application/mission_controller.py` | Add `"U": UTurn()` to command map |
| `tests/domain/test_extensible_commands.py` | New test file |

Files **not** touched:

- `mars_rover/domain/rover.py` ✅
- `mars_rover/domain/plateau.py` ✅
- `mars_rover/domain/heading.py` ✅
- `mars_rover/adapters/input_parser.py` ✅
- `mars_rover/adapters/output_formatter.py` ✅

---

## Frontend

No UI impact. The operator can include `U` in any command string once the mapping is registered.

---

## Infrastructure

No infrastructure changes.

---

## Definition of Done

- [ ] `UTurn` class added to `mars_rover/domain/commands.py`
- [ ] Command map updated in `MissionController`
- [ ] All 6 `UTurn` unit tests pass
- [ ] Zero changes to `Rover`, `Plateau`, `Heading`, or `OutputFormatter`
- [ ] All existing tests still pass (no regression)
- [ ] `ruff`, `black`, and `isort` pass with no warnings
