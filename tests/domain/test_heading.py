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


class TestHeadingDelta(unittest.TestCase):
    def test_rover_s1_given_heading_n_when_delta_then_returns_0_1(self):
        # GIVEN: Heading.N
        from mars_rover.domain.heading import Heading

        # WHEN: delta() is called
        result = Heading.N.delta()

        # THEN: Returns (0, 1)
        self.assertEqual(result, (0, 1))

    def test_rover_s1_given_heading_e_when_delta_then_returns_1_0(self):
        # GIVEN: Heading.E
        from mars_rover.domain.heading import Heading

        # WHEN / THEN
        self.assertEqual(Heading.E.delta(), (1, 0))

    def test_rover_s1_given_heading_s_when_delta_then_returns_0_minus1(self):
        # GIVEN: Heading.S
        from mars_rover.domain.heading import Heading

        # WHEN / THEN
        self.assertEqual(Heading.S.delta(), (0, -1))

    def test_rover_s1_given_heading_w_when_delta_then_returns_minus1_0(self):
        # GIVEN: Heading.W
        from mars_rover.domain.heading import Heading

        # WHEN / THEN
        self.assertEqual(Heading.W.delta(), (-1, 0))
