# Tests for hex grid functionality

import unittest
from src.core.hex_grid import HexGrid

class TestHexGrid(unittest.TestCase):
    def test_grid_generation(self):
        grid = HexGrid()
        grid.generate_hexagonal_grid(1)
        self.assertEqual(len(grid.hexes), 7)  # Center + 6 neighbors

if __name__ == "__main__":
    unittest.main()