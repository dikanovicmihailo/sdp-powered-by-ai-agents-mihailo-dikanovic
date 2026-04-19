import unittest

from mars_rover.adapters.output_formatter import OutputFormatter
from mars_rover.domain.heading import Heading
from mars_rover.domain.rover import Rover


class TestOutputFormatter(unittest.TestCase):
    def test_cli_be_002_1_s1_given_rover_at_5_1_e_when_format_then_returns_5_1_e(self):
        # GIVEN: A Rover(5, 1, Heading.E) exists
        rover = Rover(5, 1, Heading.E)

        # WHEN: OutputFormatter().format(rover) is called
        result = OutputFormatter().format(rover)

        # THEN: Returns "5 1 E"
        self.assertEqual(result, "5 1 E")

    def test_cli_story_002_s1_given_rover_at_1_3_n_when_format_then_returns_1_3_n(self):
        # GIVEN: A rover ends at x=1, y=3, heading=N
        rover = Rover(1, 3, Heading.N)

        # WHEN: OutputFormatter.format(rover) is called
        result = OutputFormatter().format(rover)

        # THEN: The returned string is "1 3 N"
        self.assertEqual(result, "1 3 N")
