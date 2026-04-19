import unittest

from mars_rover.domain.plateau import Plateau


class TestPlateauS1ValidDimensions(unittest.TestCase):
    def test_plateau_s1_given_valid_dimensions_when_constructed_then_contains_bounds(
        self,
    ):
        # GIVEN: Upper-right corner coordinates 5 5
        plateau = Plateau(5, 5)

        # WHEN: Boundary points are checked
        # THEN: Origin and upper-right corner are within bounds
        self.assertTrue(plateau.is_within(0, 0))
        self.assertTrue(plateau.is_within(5, 5))


class TestPlateauS2InteriorPoint(unittest.TestCase):
    def test_plateau_s2_given_plateau_when_interior_point_checked_then_returns_true(
        self,
    ):
        # GIVEN: A Plateau(5, 5)
        plateau = Plateau(5, 5)

        # WHEN: An interior point is checked
        # THEN: Returns True
        self.assertTrue(plateau.is_within(3, 2))
