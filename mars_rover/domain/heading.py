from enum import Enum


class Heading(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    def turn_left(self) -> "Heading":
        order = [Heading.N, Heading.W, Heading.S, Heading.E]
        return order[(order.index(self) + 1) % 4]
