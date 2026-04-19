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
