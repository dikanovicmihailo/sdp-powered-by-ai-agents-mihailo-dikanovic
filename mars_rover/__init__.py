"""Minimal Mars Rover domain helpers."""


def turn_left(heading: str) -> str:
    """Return the new heading after a 90-degree left turn."""
    order = ["N", "W", "S", "E"]
    return order[(order.index(heading) + 1) % 4]
