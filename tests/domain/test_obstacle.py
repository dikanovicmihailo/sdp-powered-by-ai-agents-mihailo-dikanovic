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

    def test_nav_story_003_s3_given_no_obstacles_when_move_forward_then_moves_normally(
        self,
    ):
        # GIVEN: Plateau with no obstacles, rover at (1,2,E)
        plateau = Plateau(5, 5)
        rover = Rover(1, 2, Heading.E)

        # WHEN: MoveForward is called
        MoveForward(plateau)(rover)

        # THEN: Rover moves normally to (2,2)
        self.assertEqual(rover.x, 2)
        self.assertEqual(rover.y, 2)

    def test_nav_story_003_s2_given_obstacle_stopped_rover_when_format_then_o_prefix(
        self,
    ):
        # GIVEN: Rover stopped by obstacle at (1,2,E)
        from mars_rover.adapters.output_formatter import OutputFormatter

        rover = Rover(1, 2, Heading.E)

        # WHEN: OutputFormatter formats with obstacle_stopped=True
        result = OutputFormatter().format(rover, obstacle_stopped=True)

        # THEN: Output has "O:" prefix
        self.assertEqual(result, "O:1 2 E")

    def test_nav_story_003_s4_given_obstacle_when_first_blocked_then_rest_skipped(
        self,
    ):
        # GIVEN: Obstacle at (2,2), rover at (1,2,E) with command "MMM"
        from mars_rover.application.mission_controller import MissionController

        plateau = Plateau(5, 5, obstacles=frozenset({(2, 2)}))
        rover = Rover(1, 2, Heading.E)
        controller = MissionController(plateau)

        # WHEN: Mission runs
        results = controller.run([(rover, "MMM")])

        # THEN: Rover never moved, obstacle_stopped is True
        final_rover, obstacle_stopped = results[0]
        self.assertTrue(obstacle_stopped)
        self.assertEqual(final_rover.x, 1)
        self.assertEqual(final_rover.y, 2)
