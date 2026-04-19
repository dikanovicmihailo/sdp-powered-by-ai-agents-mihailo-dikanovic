import unittest

from mars_rover.domain.commands import TurnLeft
from mars_rover.domain.heading import Heading
from mars_rover.domain.rover import Rover


class TestTurnLeft(unittest.TestCase):
    def test_nav_be_001_1_s1_turn_left_from_north_gives_west_position_unchanged(self):
        # GIVEN: A rover at (2, 3, N)
        rover = Rover(2, 3, Heading.N)

        # WHEN: TurnLeft() is called
        TurnLeft()(rover)

        # THEN: heading == W, position unchanged
        self.assertEqual(rover.heading, Heading.W)
        self.assertEqual(rover.x, 2)
        self.assertEqual(rover.y, 3)
