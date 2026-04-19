class Plateau:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rovers = []

    def add_rover(self, rover):
        self.rovers.append(rover)


class Rover:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


def report_positions(plateau):
    return [
        {"x": rover.x, "y": rover.y, "direction": rover.direction}
        for rover in plateau.rovers
    ]
