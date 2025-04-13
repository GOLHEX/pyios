class Hex:
    def __init__(self, q, r, terrain=None):
        self.q = q           # Axial coordinate q
        self.r = r           # Axial coordinate r
        self.terrain = terrain  # Example property (customizable)

    def __repr__(self):
        return f"Hex(q={self.q}, r={self.r}, terrain={self.terrain})"


class HexGrid:
    def __init__(self):
        # Dictionary to store hexes: key is (q, r) tuple, value is Hex object
        self.hexes = {}

    def add_hex(self, hex):
        """Add a hexagon to the grid."""
        self.hexes[(hex.q, hex.r)] = hex

    def get_hex(self, q, r):
        """Get the hexagon at coordinates (q, r), or None if it doesn’t exist."""
        return self.hexes.get((q, r))

    def generate_hexagonal_grid(self, radius):
        """
        Generate a hexagonal-shaped grid with the given radius.
        Includes all hexes where max(|q|, |r|, |s|) <= radius, with s = -q - r.
        """
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                s = -q - r
                if max(abs(q), abs(r), abs(s)) <= radius:
                    # Add a hexagon with default terrain (customize as needed)
                    self.add_hex(Hex(q, r, terrain="grass"))

    def get_neighbors(self, q, r):
        """
        Return a list of neighboring hexagons that exist in the grid.
        Uses the six direction vectors for flat-top hexagons.
        """
        # Direction vectors: (dq, dr) for the six neighbors
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        neighbors = []
        for dq, dr in directions:
            nq, nr = q + dq, r + dr
            neighbor = self.get_hex(nq, nr)
            if neighbor is not None:
                neighbors.append(neighbor)
        return neighbors

    def distance(self, q1, r1, q2, r2):
        """
        Calculate the distance between two hexagons using cube coordinates.
        Distance is the maximum of the absolute differences in q, r, and s.
        """
        s1 = -q1 - r1
        s2 = -q2 - r2
        return max(abs(q1 - q2), abs(r1 - r2), abs(s1 - s2))

    def get_hexes_within_distance(self, q, r, distance):
        """
        Return all hexagons within a given distance from (q, r) that exist in the grid.
        """
        hexes = []
        for dq in range(-distance, distance + 1):
            for dr in range(-distance, distance + 1):
                ds = -dq - dr
                if max(abs(dq), abs(dr), abs(ds)) <= distance:
                    nq, nr = q + dq, r + dr
                    hex = self.get_hex(nq, nr)
                    if hex is not None:
                        hexes.append(hex)
        return hexes


# Example usage
if __name__ == "__main__":
    # Create a hex grid
    grid = HexGrid()

    # Generate a hexagonal grid with radius 2
    grid.generate_hexagonal_grid(2)

    # Access the center hexagon
    center_hex = grid.get_hex(0, 0)
    print(center_hex)  # Output: Hex(q=0, r=0, terrain=grass)

    # Get its neighbors
    neighbors = grid.get_neighbors(0, 0)
    print(neighbors)  # List of up to 6 neighboring hexes

    # Calculate distance between (0, 0) and (1, -1)
    dist = grid.distance(0, 0, 1, -1)
    print(dist)  # Output: 1

    # Get all hexes within distance 1 from (0, 0)
    nearby = grid.get_hexes_within_distance(0, 0, 1)
    print(nearby)  # List of hexes within distance 1