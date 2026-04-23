import subprocess  # nosec B404
import sys
import unittest


class TestCLIOutput(unittest.TestCase):
    def _run_cli(self, input_text: str):
        return subprocess.run(  # nosec B603
            [sys.executable, "-m", "mars_rover"],
            input=input_text,
            capture_output=True,
            text=True,
        )

    def test_cli_story_002_s3_given_valid_input_when_cli_runs_then_output_on_stdout(
        self,
    ):
        # GIVEN: A valid mission input
        input_text = "5 5\n1 3 N\nM\n"

        # WHEN: The CLI runs
        result = self._run_cli(input_text)

        # THEN: Output appears on stdout, stderr is empty
        self.assertIn("N", result.stdout)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode, 0)
