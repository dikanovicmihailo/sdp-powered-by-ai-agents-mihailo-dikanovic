import unittest
from dataclasses import FrozenInstanceError

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


class TestPlateauS3OutOfBoundsPoint(unittest.TestCase):
    def test_plateau_s3_given_plateau_when_x_too_large_then_returns_false(self):
        # GIVEN: A Plateau(5, 5)
        plateau = Plateau(5, 5)

        # WHEN: A point with x beyond width is checked
        # THEN: Returns False
        self.assertFalse(plateau.is_within(6, 0))

    def test_plateau_s3_given_plateau_when_negative_x_then_returns_false(self):
        # GIVEN: A Plateau(5, 5)
        plateau = Plateau(5, 5)

        # WHEN: A point with negative x is checked
        # THEN: Returns False
        self.assertFalse(plateau.is_within(-1, 3))


class TestPlateauS4Immutability(unittest.TestCase):
    def test_plateau_s4_given_plateau_when_width_modified_then_raises_exception(self):
        # GIVEN: A Plateau(5, 5) has been created
        plateau = Plateau(5, 5)

        # WHEN: An attempt is made to modify width
        # THEN: An exception is raised
        with self.assertRaises(FrozenInstanceError):
            plateau.width = 10  # type: ignore[misc]
