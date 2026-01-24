import unittest

from flow_player import CellType, get_map_graph, get_map_grid


class FlowPlayerTest(unittest.TestCase):
    def test_map_zero_grid(self) -> None:
        self.assertEqual(12, get_map_grid(0).sum())

    def test_map_zero_graph(self) -> None:
        self.assertEqual(64, get_map_graph(0).number_of_nodes())

    def test_is_fireproof(self) -> None:
        self.assertTrue(CellType.WATER.is_fireproof())
        self.assertTrue(CellType.WALL.is_fireproof())
        self.assertFalse(CellType.OPEN.is_fireproof())
        self.assertFalse(CellType.FIRE.is_fireproof())
