import unittest

from fire_challenge import FireChallenge


class AvailableMapsTest(unittest.TestCase):
    def test_get_available_maps(self) -> None:
        available = FireChallenge.get_available_maps()
        self.assertGreater(len(available), 13)
        self.assertEqual((0, "Two Fires"), available[0])
