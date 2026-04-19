from dataclasses import dataclass

from mars_rover.domain.heading import Heading


@dataclass
class Rover:
    x: int
    y: int
    heading: Heading

    def execute(self, command) -> None:
        command(self)
