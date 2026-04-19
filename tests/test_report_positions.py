import unittest

from mars_rover import Plateau, Rover, report_positions


class TestReportPositions(unittest.TestCase):
    def test_report_positions(self):
        # GIVEN a plateau with two rovers at different positions
        plateau = Plateau(width=5, height=5)
        rovers = [Rover(x=1, y=2, direction="N"), Rover(x=3, y=3, direction="E")]
        for rover in rovers:
            plateau.add_rover(rover)

        # WHEN the system reports the positions
        reported = report_positions(plateau)

        # THEN the output should list the positions of both rovers correctly
        expected = [
            {"x": 1, "y": 2, "direction": "N"},
            {"x": 3, "y": 3, "direction": "E"},
        ]
        self.assertEqual(reported, expected)


if __name__ == "__main__":
    unittest.main()
