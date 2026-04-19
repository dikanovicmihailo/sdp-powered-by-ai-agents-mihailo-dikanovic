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
