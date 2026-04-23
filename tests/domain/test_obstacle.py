import unittest

from mars_rover.domain.commands import MoveForward, ObstacleEncountered
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


class TestObstacle(unittest.TestCase):
    def test_nav_be_003_s1_given_blocked_cell_when_move_forward_then_raises_obstacle(
        self,
    ):
        # GIVEN: Plateau has obstacle at (2,2), rover at (1,2,E)
        plateau = Plateau(5, 5, obstacles=frozenset({(2, 2)}))
        rover = Rover(1, 2, Heading.E)

        # WHEN: MoveForward is called
        # THEN: ObstacleEncountered is raised and position unchanged
        with self.assertRaises(ObstacleEncountered):
            MoveForward(plateau)(rover)
        self.assertEqual(rover.x, 1)
        self.assertEqual(rover.y, 2)
