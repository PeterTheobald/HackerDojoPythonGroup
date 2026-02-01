import sys
import unittest
from io import StringIO

from fire_challenge_players.example_player import solve_fire_challenge


class ExamplePlayerTest(unittest.TestCase):
    def test_example_player(self) -> None:
        console = sys.stdin
        sys.stdout = StringIO()  # /dev/null, for chatty target code
        try:
            solve_fire_challenge(visualize=False)
            self.assertGreater(len(sys.stdout.getvalue()), 440)
        finally:
            sys.stdout = console
