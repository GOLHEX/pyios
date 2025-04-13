
import os

# Define the project structure as a dictionary
project_structure = {
    "hex_game_engine": {
        "main.py": "# Entry point to run the game\n\nif __name__ == '__main__':\n    print('Game starting...')",
        "README.md": "# Hex Game Engine\n\nA hexagonal grid-based game engine built in Python.",
        "requirements.txt": "# Dependencies\n# pygame==2.5.2",
        "src": {
            "__init__.py": "",
            "core": {
                "__init__.py": "",
                "hex_grid.py": "# Hex and HexGrid classes\n\nclass Hex:\n    pass\n\nclass HexGrid:\n    pass",
                "game_logic.py": "# Game rules and mechanics\n\nclass GameLogic:\n    pass"
            },
            "rendering": {
                "__init__.py": "",
                "renderer.py": "# Handles drawing the grid (e.g., with Pygame)\n\nclass Renderer:\n    pass"
            },
            "utils": {
                "__init__.py": "",
                "helpers.py": "# Math, coordinate conversions, etc.\n\ndef hex_to_pixel(q, r, size=30):\n    pass"
            }
        },
        "assets": {
            "hex_grass.png": None,  # Placeholder for binary file (won't write content)
            "hex_water.png": None   # Placeholder for binary file (won't write content)
        },
        "tests": {
            "__init__.py": "",
            "test_hex_grid.py": "# Tests for hex grid functionality\n\nimport unittest\n\nclass TestHexGrid(unittest.TestCase):\n    def test_placeholder(self):\n        pass"
        }
    }
}

def create_structure(base_path, structure):
    """
    Recursively create directories and files based on the provided structure.
    """
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            # Create directory and recurse
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # Create file
            if not os.path.exists(path):
                if content is None:
                    # For binary files like .png, just create an empty file (no content)
                    with open(path, "wb") as f:
                        pass
                else:
                    # Write text content to the file
                    with open(path, "w") as f:
                        f.write(content)
            print(f"Created: {path}")

def main():
    # Get the current working directory
    base_dir = os.getcwd()
    
    # Create the project structure
    print("Creating project structure...")
    create_structure(base_dir, project_structure)
    print("\nProject structure created successfully!")
    print("Directory: ", os.path.join(base_dir, "hex_game_engine"))

if __name__ == "__main__":
    main()