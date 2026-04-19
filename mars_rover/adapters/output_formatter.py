from mars_rover.domain.rover import Rover


class OutputFormatter:
    def format(self, rover: Rover) -> str:
        return f"{rover.x} {rover.y} {rover.heading.value}"
