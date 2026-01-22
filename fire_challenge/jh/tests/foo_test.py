import unittest

from example_player import solve_fire_challenge


class FooTest(unittest.TestCase):
    def test_example_player(self) -> None:
        solve_fire_challenge(visualize=False)
