from dataclasses import dataclass, field


@dataclass(frozen=True)
class Plateau:
    """Immutable rectangular grid. Lower-left is always (0, 0)."""

    width: int
    height: int
    obstacles: frozenset = field(default_factory=frozenset)

    def is_within(self, x: int, y: int) -> bool:
        return 0 <= x <= self.width and 0 <= y <= self.height

    def is_blocked(self, x: int, y: int) -> bool:
        return (x, y) in self.obstacles
