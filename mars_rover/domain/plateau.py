from dataclasses import dataclass


@dataclass(frozen=True)
class Plateau:
    """Immutable rectangular grid. Lower-left is always (0, 0)."""

    width: int
    height: int
