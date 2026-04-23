from collections.abc import Sequence

from mars_rover.domain.commands import (
    MoveForward,
    ObstacleEncountered,
    TurnLeft,
    TurnRight,
)
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


class MissionController:
    def __init__(self, plateau: Plateau) -> None:
        self._plateau = plateau

    def run(self, missions: Sequence[tuple[Rover, str]]) -> list[tuple[Rover, bool]]:
        command_map = {
            "L": TurnLeft(),
            "R": TurnRight(),
            "M": MoveForward(self._plateau),
        }
        results: list[tuple[Rover, bool]] = []
        for rover, command_string in missions:
            obstacle_stopped = False
            for ch in command_string:
                try:
                    rover.execute(command_map[ch])
                except ObstacleEncountered:
                    obstacle_stopped = True
                    break
            results.append((rover, obstacle_stopped))
        return results
