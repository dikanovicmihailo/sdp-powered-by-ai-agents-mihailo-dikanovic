import unittest

from mars_rover.adapters.input_parser import InputParser
from mars_rover.domain.heading import Heading
from mars_rover.domain.plateau import Plateau

KATA_INPUT = "5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM\n"


class TestInputParser(unittest.TestCase):
    def test_cli_story_001_s1_given_valid_input_when_parse_called_then_returns_plateau(
        self,
    ):
        # GIVEN: Valid input text with plateau + 2 rovers
        parser = InputParser()

        # WHEN: InputParser.parse() is called
        plateau, _ = parser.parse(KATA_INPUT)

        # THEN: Returns a Plateau with correct dimensions
        self.assertEqual(plateau, Plateau(5, 5))

    def test_cli_story_001_s2_given_kata_input_when_parse_called_then_two_missions(
        self,
    ):
        # GIVEN: Kata example input
        parser = InputParser()

        # WHEN: InputParser.parse() is called
        _, missions = parser.parse(KATA_INPUT)

        # THEN: Returns two (Rover, command_string) pairs with correct values
        self.assertEqual(len(missions), 2)
        rover1, cmd1 = missions[0]
        self.assertEqual(rover1.x, 1)
        self.assertEqual(rover1.y, 2)
        self.assertEqual(rover1.heading, Heading.N)
        self.assertEqual(cmd1, "LMLMLMLMM")
        rover2, cmd2 = missions[1]
        self.assertEqual(rover2.x, 3)
        self.assertEqual(rover2.y, 3)
        self.assertEqual(rover2.heading, Heading.E)
        self.assertEqual(cmd2, "MMRMMRMRRM")
