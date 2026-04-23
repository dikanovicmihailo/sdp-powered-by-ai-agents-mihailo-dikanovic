from mars_rover.domain.rover import Rover


class OutputFormatter:
    def format(self, rover: Rover, obstacle_stopped: bool = False) -> str:
        prefix = "O:" if obstacle_stopped else ""
        return f"{prefix}{rover.x} {rover.y} {rover.heading.value}"
