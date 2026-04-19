import unittest

from mars_rover.domain.commands import MoveForward, TurnLeft, TurnRight
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
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


class TestTurnRight(unittest.TestCase):
    def test_nav_story_001_s2_turn_right_from_north_gives_east_position_unchanged(self):
        # GIVEN: A rover at (1, 2, N)
        rover = Rover(1, 2, Heading.N)

        # WHEN: TurnRight() is called
        TurnRight()(rover)

        # THEN: heading == E, position unchanged
        self.assertEqual(rover.heading, Heading.E)
        self.assertEqual(rover.x, 1)
        self.assertEqual(rover.y, 2)


class TestMoveForward(unittest.TestCase):
    def test_nav_story_001_s3_move_forward_north_advances_y(self):
        # GIVEN: A rover at (1, 2, N) on plateau 5 5
        plateau = Plateau(5, 5)
        rover = Rover(1, 2, Heading.N)

        # WHEN: MoveForward is called
        MoveForward(plateau)(rover)

        # THEN: rover is at (1, 3, N)
        self.assertEqual(rover.x, 1)
        self.assertEqual(rover.y, 3)
        self.assertEqual(rover.heading, Heading.N)


class TestKataExamples(unittest.TestCase):
    def _run(self, rover, commands, plateau):
        mapping = {
            "L": TurnLeft(),
            "R": TurnRight(),
            "M": MoveForward(plateau),
        }
        for ch in commands:
            rover.execute(mapping[ch])
        return rover

    def test_nav_story_001_s4_kata_example_1_lmlmlmlmm_from_1_2_n(self):
        # GIVEN: A rover at (1, 2, N) on plateau 5 5
        plateau = Plateau(5, 5)
        rover = Rover(1, 2, Heading.N)

        # WHEN: Command string LMLMLMLMM is executed
        result = self._run(rover, "LMLMLMLMM", plateau)

        # THEN: Rover ends at (1, 3, N)
        self.assertEqual(result.x, 1)
        self.assertEqual(result.y, 3)
        self.assertEqual(result.heading, Heading.N)

    def test_nav_story_001_s5_kata_example_2_mmrmmrmrrm_from_3_3_e(self):
        # GIVEN: A rover at (3, 3, E) on plateau 5 5
        plateau = Plateau(5, 5)
        rover = Rover(3, 3, Heading.E)

        # WHEN: Command string MMRMMRMRRM is executed
        result = self._run(rover, "MMRMMRMRRM", plateau)

        # THEN: Rover ends at (5, 1, E)
        self.assertEqual(result.x, 5)
        self.assertEqual(result.y, 1)
        self.assertEqual(result.heading, Heading.E)
