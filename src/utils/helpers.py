# src/utils/helpers.py

from collections import namedtuple
import math
from src.utils.hex_utils import Layout, layout_flat, Point, Hex  # Импортируем Layout, layout_flat, Point и новый Hex

# Конфигурация Layout
HEX_SIZE = 21
layout = Layout(
    orientation=layout_flat,
    size=Point(HEX_SIZE, HEX_SIZE),
    origin=Point(0, 0)
)

# Обёртки для преобразований, используя методы нового класса Hex:

def hex_to_pixel(layout, h: Hex) -> Point:
    """Преобразует кубические координаты h в пиксельные, вызывая метод to_pixel."""
    return h.to_pixel(layout)

def pixel_to_hex(layout, p: Point) -> Hex:
    """Преобразует пиксельные координаты в кубические, используя обратное преобразование."""
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    pt = Point((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
    q = M.b0 * pt.x + M.b1 * pt.y
    r = M.b2 * pt.x + M.b3 * pt.y
    return Hex.round(Hex(q, r, -q - r))

def polygon_corners(layout, h: Hex):
    """Возвращает углы шестиугольника h для отрисовки."""
    return h.polygon_corners(layout)

def get_hex_corners(q, r, s):
    """
    Возвращает список углов шестиугольника в пиксельных координатах для Hex(q, r, s).
    """
    try:
        hex_obj = Hex(q, r, s)
        corners = polygon_corners(layout, hex_obj)
        if corners is None:
            return []
        return corners
    except Exception as e:
        return []
