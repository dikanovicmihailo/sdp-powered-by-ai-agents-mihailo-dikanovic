from collections.abc import Sequence

from mars_rover.domain.commands import MoveForward, TurnLeft, TurnRight
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


class MissionController:
    def __init__(self, plateau: Plateau) -> None:
        self._plateau = plateau

    def run(self, missions: Sequence[tuple[Rover, str]]) -> list[Rover]:
        command_map = {
            "L": TurnLeft(),
            "R": TurnRight(),
            "M": MoveForward(self._plateau),
        }
        for rover, command_string in missions:
            for ch in command_string:
                rover.execute(command_map[ch])
        return [rover for rover, _ in missions]
