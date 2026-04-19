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


class TestHeadingTurnLeftFullCircle(unittest.TestCase):
    def test_rover_be_001_s2_given_heading_n_when_turn_left_four_times_then_returns_n(
        self,
    ):
        # GIVEN: Starting heading Heading.N
        from mars_rover.domain.heading import Heading

        h = Heading.N

        # WHEN: turn_left() is called four times
        for _ in range(4):
            h = h.turn_left()

        # THEN: The final heading is Heading.N
        self.assertEqual(h, Heading.N)


class TestHeadingTurnRight(unittest.TestCase):
    def test_rover_s2_given_heading_n_when_turn_right_then_returns_e(self):
        # GIVEN: Heading.N
        from mars_rover.domain.heading import Heading

        # WHEN: turn_right() is called
        result = Heading.N.turn_right()

        # THEN: Returns Heading.E
        self.assertEqual(result, Heading.E)
