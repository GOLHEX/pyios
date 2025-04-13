###/main.py
from src.core.hex_grid import HexGrid
from src.rendering.renderer import Renderer
import time

def main():
    # Инициализация сетки
    grid = HexGrid()
    grid.generate_hexagonal_grid(radius=3)  # Убедитесь, что эта строка присутствует

    # Инициализация рендерера
    renderer = Renderer(grid, screen_width=1024, screen_height=1024, hex_size=21)
    renderer.run()

if __name__ == "__main__":
    main()

    