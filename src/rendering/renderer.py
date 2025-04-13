import pygame
from src.utils.helpers import hex_to_pixel, get_hex_corners, pixel_to_hex

class Renderer:
    def __init__(self, grid, screen_width=800, screen_height=600, hex_size=30):
        self.grid = grid
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.hex_size = hex_size

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Hex Grid Game")
        self.running = True

        # Terrain colors
        self.terrain_colors = {
            "grass": (0, 128, 0),  # Green
            "water": (0, 0, 255),  # Blue
            None: (200, 200, 200)  # Gray for undefined terrain
        }

        # Highlight color for the selected hex
        self.highlight_color = (255, 255, 0)  # Yellow

        # Track the currently selected hex (q, r) or None if none selected
        self.selected_hex = None

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle mouse click
                    self.handle_mouse_click(event.pos)

            # Clear the screen
            self.screen.fill((255, 255, 255))  # White background

            # Draw the grid
            self.draw_grid()

            # Update the display
            pygame.display.flip()

        # Cleanup
        pygame.quit()

    def handle_mouse_click(self, pos):
        """
        Handle a mouse click at the given pixel position (x, y).
        Convert to hex coordinates and select the clicked hex if it exists.
        """
        # Get the pixel coordinates adjusted for the offset
        offset_x = self.screen_width // 2
        offset_y = self.screen_height // 2
        x, y = pos
        x -= offset_x  # Remove the centering offset
        y -= offset_y

        # Convert pixel coordinates to hex coordinates
        q, r = pixel_to_hex(x, y, self.hex_size)

        # Check if the hex exists in the grid
        if self.grid.get_hex(q, r) is not None:
            self.selected_hex = (q, r)
            print(f"Selected hex: (q={q}, r={r})")
        else:
            self.selected_hex = None  # Deselect if clicked outside the grid

    def draw_grid(self):
        # Center the grid by offsetting all coordinates
        offset_x = self.screen_width // 2
        offset_y = self.screen_height // 2

        for hex in self.grid.hexes.values():
            # Convert hex coordinates to pixel coordinates
            x, y = hex_to_pixel(hex.q, hex.r, self.hex_size)

            # Apply offset to center the grid
            x += offset_x
            y += offset_y

            # Get the hexagon's corners
            corners = get_hex_corners(x, y, self.hex_size)

            # Determine the color
            if self.selected_hex and (hex.q, hex.r) == self.selected_hex:
                color = self.highlight_color  # Highlight selected hex
            else:
                color = self.terrain_colors.get(hex.terrain, self.terrain_colors[None])

            # Draw the hexagon (filled)
            pygame.draw.polygon(self.screen, color, corners)

            # Draw the hexagon outline
            pygame.draw.polygon(self.screen, (0, 0, 0), corners, 1)  # Black outline