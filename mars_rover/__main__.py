import sys

from mars_rover.adapters.input_parser import InputParser
from mars_rover.adapters.output_formatter import OutputFormatter
from mars_rover.application.mission_controller import MissionController


def main() -> None:
    text = sys.stdin.read()
    if not text.strip():
        return
    try:
        parser = InputParser()
        plateau, missions = parser.parse(text)
    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        sys.exit(1)

    controller = MissionController(plateau)
    formatter = OutputFormatter()
    for rover, obstacle_stopped in controller.run(missions):
        print(formatter.format(rover, obstacle_stopped=obstacle_stopped))


if __name__ == "__main__":
    main()
