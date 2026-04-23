import unittest

from mars_rover.domain.commands import UTurn
from mars_rover.domain.heading import Heading
from mars_rover.domain.rover import Rover


class TestExtensibleCommands(unittest.TestCase):
    def test_nav_story_004_s1_given_rover_facing_north_when_uturn_then_faces_south(
        self,
    ):
        # GIVEN: Rover facing North
        rover = Rover(0, 0, Heading.N)

        # WHEN: UTurn is executed
        UTurn()(rover)

        # THEN: Rover faces South
        self.assertEqual(rover.heading, Heading.S)

    def test_nav_be_004_s1_given_rover_facing_east_when_uturn_then_faces_west(self):
        # GIVEN: Rover facing East
        rover = Rover(0, 0, Heading.E)

        # WHEN: UTurn is executed
        UTurn()(rover)

        # THEN: Rover faces West
        self.assertEqual(rover.heading, Heading.W)
