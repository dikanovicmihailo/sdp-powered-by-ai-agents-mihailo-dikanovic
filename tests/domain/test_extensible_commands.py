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

    def test_nav_be_004_s1_given_rover_facing_south_when_uturn_then_faces_north(self):
        # GIVEN: Rover facing South
        rover = Rover(0, 0, Heading.S)

        # WHEN: UTurn is executed
        UTurn()(rover)

        # THEN: Rover faces North
        self.assertEqual(rover.heading, Heading.N)

    def test_nav_be_004_s1_given_rover_facing_west_when_uturn_then_faces_east(self):
        # GIVEN: Rover facing West
        rover = Rover(0, 0, Heading.W)

        # WHEN: UTurn is executed
        UTurn()(rover)

        # THEN: Rover faces East
        self.assertEqual(rover.heading, Heading.E)

    def test_nav_story_004_s1_given_rover_at_position_when_uturn_then_no_move(
        self,
    ):
        # GIVEN: Rover at (3,4,N)
        rover = Rover(3, 4, Heading.N)

        # WHEN: UTurn is executed
        UTurn()(rover)

        # THEN: Position unchanged
        self.assertEqual(rover.x, 3)
        self.assertEqual(rover.y, 4)

    def test_nav_story_004_s3_given_uturn_registered_when_rover_executes_then_rotates(
        self,
    ):
        # GIVEN: Rover facing North
        rover = Rover(0, 0, Heading.N)

        # WHEN: UTurn dispatched via rover.execute()
        rover.execute(UTurn())

        # THEN: Rover faces South
        self.assertEqual(rover.heading, Heading.S)
