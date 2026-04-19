from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mars_rover.domain.rover import Rover


class TurnLeft:
    def __call__(self, rover: Rover) -> None:
        rover.heading = rover.heading.turn_left()


class TurnRight:
    def __call__(self, rover: Rover) -> None:
        rover.heading = rover.heading.turn_right()
