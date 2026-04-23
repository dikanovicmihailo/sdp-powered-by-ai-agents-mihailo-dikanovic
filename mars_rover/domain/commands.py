from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mars_rover.domain.plateau import Plateau
    from mars_rover.domain.rover import Rover


class ObstacleEncountered(Exception):  # noqa: N818
    """Raised when MoveForward would enter an obstacle cell."""


class TurnLeft:
    def __call__(self, rover: Rover) -> None:
        rover.heading = rover.heading.turn_left()


class TurnRight:
    def __call__(self, rover: Rover) -> None:
        rover.heading = rover.heading.turn_right()


class MoveForward:
    def __init__(self, plateau: Plateau) -> None:
        self._plateau = plateau

    def __call__(self, rover: Rover) -> None:
        dx, dy = rover.heading.delta()
        new_x, new_y = rover.x + dx, rover.y + dy
        if not self._plateau.is_within(new_x, new_y):
            return
        if self._plateau.is_blocked(new_x, new_y):
            raise ObstacleEncountered()
        rover.x = new_x
        rover.y = new_y
