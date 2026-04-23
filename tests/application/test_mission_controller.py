import unittest

from mars_rover.application.mission_controller import MissionController
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau
from mars_rover.domain.rover import Rover


class TestMissionStory001S1(unittest.TestCase):
    def test_s1_given_two_rovers_when_mission_runs_then_each_processes_own_commands(
        self,
    ):
        # GIVEN: Two rovers with separate command strings
        plateau = Plateau(5, 5)
        rover1 = Rover(1, 2, Heading.N)
        rover2 = Rover(3, 3, Heading.E)
        controller = MissionController(plateau)

        # WHEN: The mission runs
        results = controller.run([(rover1, "L"), (rover2, "R")])

        # THEN: Each rover processed its own command independently
        self.assertEqual(results[0].heading, Heading.W)  # rover1 turned left
        self.assertEqual(results[1].heading, Heading.S)  # rover2 turned right
