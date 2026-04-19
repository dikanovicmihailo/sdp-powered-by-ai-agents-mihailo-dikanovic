import unittest


class TestHeadingTurnLeft(unittest.TestCase):
    def test_rover_be_001_s1_given_heading_n_when_turn_left_then_returns_w(self):
        # GIVEN: Heading.N exists
        from mars_rover.domain.heading import Heading

        # WHEN: turn_left() is called
        result = Heading.N.turn_left()

        # THEN: Returns Heading.W and original is unchanged
        self.assertEqual(result, Heading.W)
        self.assertEqual(Heading.N, Heading.N)
