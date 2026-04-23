import subprocess  # nosec B404
import sys
import unittest


def _run(input_text: str):
    return subprocess.run(  # nosec B603
        [sys.executable, "-m", "mars_rover"],
        input=input_text,
        capture_output=True,
        text=True,
    )


class TestCLIErrors(unittest.TestCase):
    def test_cli_story_003_s1_given_missing_plateau_height_when_cli_runs_then_exits_1(
        self,
    ):
        # GIVEN: Plateau line is missing height
        # WHEN: CLI runs
        result = _run("5\n1 2 N\nM\n")

        # THEN: Exit code is 1 and stderr contains descriptive message
        self.assertEqual(result.returncode, 1)
        self.assertIn("Input error", result.stderr)
        self.assertIn("Plateau", result.stderr)

    def test_cli_story_003_s2_given_invalid_heading_when_cli_runs_then_exits_1(self):
        # GIVEN: Rover line has invalid heading "X"
        # WHEN: CLI runs
        result = _run("5 5\n1 2 X\nM\n")

        # THEN: Exit code is 1 and stderr contains descriptive message
        self.assertEqual(result.returncode, 1)
        self.assertIn("Input error", result.stderr)
        self.assertIn("heading", result.stderr.lower())
