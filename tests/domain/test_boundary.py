import unittest

from mars_rover.domain.commands import MoveForward, TurnRight
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


class TestBoundarySafeStop(unittest.TestCase):
    def setUp(self):
        self.plateau = Plateau(5, 5)

    def test_nav_story_002_s1_given_rover_at_south_boundary_when_move_then_stays(self):
        # GIVEN: a rover at (0, 0, S) on plateau 5 5
        rover = Rover(0, 0, Heading.S)
        # WHEN: command M is executed
        MoveForward(self.plateau)(rover)
        # THEN: rover stays at (0, 0, S) and no exception is raised
        self.assertEqual(rover.x, 0)
        self.assertEqual(rover.y, 0)

    def test_nav_story_002_s2_given_rover_at_north_boundary_when_move_then_stays(self):
        # GIVEN: a rover at (5, 5, N) on plateau 5 5
        rover = Rover(5, 5, Heading.N)
        # WHEN: command M is executed
        MoveForward(self.plateau)(rover)
        # THEN: rover stays at (5, 5, N) and no exception is raised
        self.assertEqual(rover.x, 5)
        self.assertEqual(rover.y, 5)

    def test_nav_story_002_s3_given_rover_at_west_boundary_when_move_then_stays(self):
        # GIVEN: a rover at (0, 0, W) on plateau 5 5
        rover = Rover(0, 0, Heading.W)
        # WHEN: command M is executed
        MoveForward(self.plateau)(rover)
        # THEN: rover stays at (0, 0, W) and no exception is raised
        self.assertEqual(rover.x, 0)
        self.assertEqual(rover.y, 0)

    def test_nav_story_002_s4_given_rover_at_east_boundary_when_move_then_stays(self):
        # GIVEN: a rover at (5, 0, E) on plateau 5 5
        rover = Rover(5, 0, Heading.E)
        # WHEN: command M is executed
        MoveForward(self.plateau)(rover)
        # THEN: rover stays at (5, 0, E) and no exception is raised
        self.assertEqual(rover.x, 5)
        self.assertEqual(rover.y, 0)

    def test_nav_story_002_s5_given_boundary_hit_when_move_then_no_exception_raised(
        self,
    ):
        # GIVEN: a rover at (0, 0, S) on plateau 5 5
        rover = Rover(0, 0, Heading.S)
        # WHEN: command M is executed at boundary
        # THEN: no exception propagates
        try:
            MoveForward(self.plateau)(rover)
        except Exception as exc:
            self.fail(f"MoveForward raised unexpectedly: {exc}")

    def test_nav_story_002_s5b_given_safe_stop_when_subsequent_cmds_then_moves(
        self,
    ):
        # GIVEN: a rover at (0, 0, S) that safe-stops at boundary
        rover = Rover(0, 0, Heading.S)
        move = MoveForward(self.plateau)
        move(rover)  # safe-stop: stays at (0, 0, S)
        # WHEN: rover turns to face north and moves
        TurnRight()(rover)  # now facing W
        TurnRight()(rover)  # now facing N
        move(rover)  # valid move: goes to (0, 1, N)
        # THEN: rover moved to (0, 1, N)
        self.assertEqual(rover.x, 0)
        self.assertEqual(rover.y, 1)
        self.assertEqual(rover.heading, Heading.N)
