from dataclasses import dataclass


@dataclass(frozen=True)
class Plateau:
    """Immutable rectangular grid. Lower-left is always (0, 0)."""

    width: int
    height: int

    def is_within(self, x: int, y: int) -> bool:
        return 0 <= x <= self.width and 0 <= y <= self.height
