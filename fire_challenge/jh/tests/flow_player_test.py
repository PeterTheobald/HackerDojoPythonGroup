import unittest

from flow_player import get_map_grid


class FlowPlayerTest(unittest.TestCase):
    def test_map_zero(self) -> None:
        self.assertEqual(12, get_map_grid(0).sum())
