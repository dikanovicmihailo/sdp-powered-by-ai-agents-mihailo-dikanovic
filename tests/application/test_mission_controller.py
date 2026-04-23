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


class TestMissionStory001S2(unittest.TestCase):
    def test_s2_given_rover1_finishes_when_rover2_starts_then_rover2_uses_own_position(
        self,
    ):
        # GIVEN: Rover 1 at boundary, Rover 2 at its own start
        plateau = Plateau(5, 5)
        rover1 = Rover(5, 5, Heading.N)
        rover2 = Rover(0, 0, Heading.E)
        controller = MissionController(plateau)

        # WHEN: Mission runs
        results = controller.run([(rover1, "M"), (rover2, "M")])

        # THEN: Rover 2 starts from its own position, unaffected by rover 1
        self.assertEqual(results[1].x, 1)
        self.assertEqual(results[1].y, 0)


class TestMissionStory001S3(unittest.TestCase):
    def test_s3_given_two_rovers_when_output_produced_then_one_result_per_rover(
        self,
    ):
        # GIVEN: Two rovers complete their missions
        plateau = Plateau(5, 5)
        rover1 = Rover(1, 2, Heading.N)
        rover2 = Rover(3, 3, Heading.E)
        controller = MissionController(plateau)

        # WHEN: Mission runs
        results = controller.run([(rover1, ""), (rover2, "")])

        # THEN: Two results in deployment order
        self.assertEqual(len(results), 2)
        self.assertIs(results[0], rover1)
        self.assertIs(results[1], rover2)


class TestMissionStory001S4(unittest.TestCase):
    def test_s4_given_kata_input_when_mission_runs_then_correct_final_positions(
        self,
    ):
        # GIVEN: Kata example — plateau 5x5, two rovers with full command strings
        plateau = Plateau(5, 5)
        missions = [
            (Rover(1, 2, Heading.N), "LMLMLMLMM"),
            (Rover(3, 3, Heading.E), "MMRMMRMRRM"),
        ]
        controller = MissionController(plateau)

        # WHEN: Mission runs
        results = controller.run(missions)

        # THEN: Rover 1 ends at 1 3 N, Rover 2 ends at 5 1 E
        self.assertEqual(results[0].x, 1)
        self.assertEqual(results[0].y, 3)
        self.assertEqual(results[0].heading, Heading.N)
        self.assertEqual(results[1].x, 5)
        self.assertEqual(results[1].y, 1)
        self.assertEqual(results[1].heading, Heading.E)
