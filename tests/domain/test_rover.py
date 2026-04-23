import unittest


class TestRoverInitialState(unittest.TestCase):
    def test_rover_s1_given_position_1_2_n_when_constructed_then_state_is_correct(
        self,
    ):
        # GIVEN: Starting position 1 2 N
        from mars_rover.domain.heading import Heading
        from mars_rover.domain.rover import Rover

        # WHEN: A Rover is constructed
        rover = Rover(1, 2, Heading.N)

        # THEN: x==1, y==2, heading==Heading.N
        self.assertEqual(rover.x, 1)
        self.assertEqual(rover.y, 2)
        self.assertEqual(rover.heading, Heading.N)


class TestRoverAllHeadings(unittest.TestCase):
    def test_rover_s2_given_any_cardinal_heading_when_constructed_then_stored_correctly(
        self,
    ):
        # GIVEN: Any valid heading (N, E, S, W)
        from mars_rover.domain.heading import Heading
        from mars_rover.domain.rover import Rover

        # WHEN / THEN: Each heading is stored correctly
        for heading in Heading:
            rover = Rover(0, 0, heading)
            self.assertEqual(rover.heading, heading)


class TestRoverExecute(unittest.TestCase):
    def test_rover_s3_given_rover_when_execute_called_with_command_then_command_applied(
        self,
    ):
        # GIVEN: A Rover(1, 2, Heading.N)
        from mars_rover.domain.heading import Heading
        from mars_rover.domain.rover import Rover

        rover = Rover(1, 2, Heading.N)

        # WHEN: execute() is called with a callable that mutates heading
        rover.execute(lambda r: setattr(r, "heading", Heading.E))

        # THEN: heading is updated
        self.assertEqual(rover.heading, Heading.E)
