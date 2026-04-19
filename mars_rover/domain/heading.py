from enum import Enum


class Heading(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    def turn_left(self) -> "Heading":
        order = [Heading.N, Heading.W, Heading.S, Heading.E]
        return order[(order.index(self) + 1) % 4]

    def turn_right(self) -> "Heading":
        order = [Heading.N, Heading.E, Heading.S, Heading.W]
        return order[(order.index(self) + 1) % 4]

    def delta(self) -> tuple[int, int]:
        return {
            Heading.N: (0, 1),
            Heading.E: (1, 0),
            Heading.S: (0, -1),
            Heading.W: (-1, 0),
        }[self]
