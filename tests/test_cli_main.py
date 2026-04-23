import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

from mars_rover import __main__ as cli


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.old_stdin = sys.stdin

    def tearDown(self):
        sys.stdin = self.old_stdin

    def _run_cli(self, input_data: str):
        sys.stdin = io.StringIO(input_data)
        out = io.StringIO()

        with redirect_stdout(out):
            try:
                cli.main()
            except SystemExit as e:
                return e.code, out.getvalue()

        return 0, out.getvalue()

    # ─────────────────────────────────────────────
    # Happy path
    # ─────────────────────────────────────────────
    def test_cli_main_end_to_end_prints_expected_position(self):
        input_data = "5 5\n1 2 N\nLMLMLMLMM\n"

        code, output = self._run_cli(input_data)

        self.assertEqual(code, 0)
        self.assertIn("1 3 N", output.strip())

    # ─────────────────────────────────────────────
    # Empty input
    # ─────────────────────────────────────────────
    def test_cli_main_with_empty_input_exits_zero(self):
        code, output = self._run_cli("")

        self.assertEqual(code, 0)
        self.assertEqual(output.strip(), "")

    # ─────────────────────────────────────────────
    # Invalid input
    # ─────────────────────────────────────────────
    def test_cli_main_with_bad_input_exits_one_and_prints_error(self):
        bad_input = "not a plateau line\n"

        sys.stdin = io.StringIO(bad_input)
        stderr = io.StringIO()

        with redirect_stderr(stderr):
            try:
                cli.main()
            except SystemExit as exc:
                self.assertEqual(exc.code, 1)

        self.assertIn("Input error", stderr.getvalue())
