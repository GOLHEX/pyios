from src.core.hex_grid import HexGrid
from src.rendering.renderer import Renderer

def main():
    # Initialize the grid
    grid = HexGrid()
    grid.generate_hexagonal_grid(radius=13)

    # Initialize the renderer
    renderer = Renderer(grid, screen_width=1024, screen_height=1024, hex_size=21)
    renderer.run()

if __name__ == "__main__":
    main()