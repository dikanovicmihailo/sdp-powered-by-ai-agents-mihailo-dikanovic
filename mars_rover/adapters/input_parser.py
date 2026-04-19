from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


class InputParser:
    def parse(self, text: str) -> tuple[Plateau, list[tuple[Rover, str]]]:
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        plateau = self._parse_plateau(lines[0])
        missions: list[tuple[Rover, str]] = []
        for i in range(1, len(lines), 2):
            rover = self._parse_rover(lines[i])
            command_string = lines[i + 1]
            missions.append((rover, command_string))
        return plateau, missions

    def _parse_plateau(self, line: str) -> Plateau:
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Plateau line must be 'WIDTH HEIGHT', got: {line!r}")
        try:
            width, height = int(parts[0]), int(parts[1])
        except ValueError as err:
            raise ValueError(
                f"Plateau dimensions must be integers, got: {line!r}"
            ) from err
        if width < 0 or height < 0:
            raise ValueError(f"Plateau dimensions must be non-negative, got: {line!r}")
        return Plateau(width, height)

    def _parse_rover(self, line: str) -> Rover:
        parts = line.split()
        if len(parts) != 3:
            raise ValueError(f"Rover line must be 'X Y HEADING', got: {line!r}")
        try:
            x, y = int(parts[0]), int(parts[1])
        except ValueError as err:
            raise ValueError(
                f"Rover coordinates must be integers, got: {line!r}"
            ) from err
        try:
            heading = Heading(parts[2])
        except ValueError as err:
            raise ValueError(
                f"Invalid heading {parts[2]!r}. Must be one of N, E, S, W."
            ) from err
        return Rover(x, y, heading)
