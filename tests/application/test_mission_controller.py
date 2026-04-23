import unittest

from mars_rover.application.mission_controller import MissionController
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


class TestMissionController(unittest.TestCase):
    def test_nav_be_003_s2_given_obstacle_when_mission_runs_then_rover_stops(self):
        # GIVEN: Rover encounters obstacle at (2,2) during command sequence
        plateau = Plateau(5, 5, obstacles=frozenset({(2, 2)}))
        rover = Rover(1, 2, Heading.E)
        controller = MissionController(plateau)

        # WHEN: MissionController.run() processes the mission
        results = controller.run([(rover, "MMM")])

        # THEN: Rover stopped, obstacle_stopped flag is True, position unchanged
        final_rover, obstacle_stopped = results[0]
        self.assertTrue(obstacle_stopped)
        self.assertEqual(final_rover.x, 1)
        self.assertEqual(final_rover.y, 2)
