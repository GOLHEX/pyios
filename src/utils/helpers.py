# Math, coordinate conversions, etc.
import math
import math

def hex_to_pixel(q, r, size=30):
    """
    Convert hex coordinates (q, r) to pixel coordinates (x, y) for flat-top hexagons.
    """
    x = size * (3/2 * q)
    y = size * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
    return x, y

def get_hex_corners(center_x, center_y, size):
    """
    Return the six corners of a flat-top hexagon centered at (center_x, center_y).
    """
    corners = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        x = center_x + size * math.cos(angle_rad)
        y = center_y + size * math.sin(angle_rad)
        corners.append((x, y))
    return corners

def pixel_to_hex(x, y, size=30):
    """
    Convert pixel coordinates (x, y) to hex coordinates (q, r) for flat-top hexagons.
    Returns the nearest hex coordinates as a (q, r) tuple.
    """
    # Inverse of hex_to_pixel
    q = (2/3 * x) / size
    r = (-1/3 * x + math.sqrt(3)/3 * y) / size

    # Convert to cube coordinates for rounding
    s = -q - r

    # Round to the nearest hex
    q = round(q)
    r = round(r)
    s = round(s)

    # Correct for rounding errors by finding the closest hex
    q_diff = abs(q - (2/3 * x) / size)
    r_diff = abs(r - (-1/3 * x + math.sqrt(3)/3 * y) / size)
    s_diff = abs(s - (-q - r))

    if q_diff > r_diff and q_diff > s_diff:
        q = -r - s
    elif r_diff > s_diff:
        r = -q - s
    else:
        s = -q - r

    return q, r