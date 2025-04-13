from __future__ import annotations
import math
from typing import List, Optional
from collections import namedtuple

# Определяем Point — просто именованный кортеж для пиксельных координат.
Point = namedtuple("Point", ["x", "y"])

# Определяем Orientation и Layout для преобразования между кубическими координатами и пикселями.
Orientation = namedtuple("Orientation", [
    "f0", "f1", "f2", "f3",
    "b0", "b1", "b2", "b3",
    "start_angle"
])
Layout = namedtuple("Layout", ["orientation", "size", "origin"])

# Примеры предопределённых ориентаций: "pointy-topped" и "flat-topped"
layout_pointy = Orientation(
    f0=math.sqrt(3.0), f1=math.sqrt(3.0) / 2.0,
    f2=0.0, f3=3.0 / 2.0,
    b0=math.sqrt(3.0) / 3.0, b1=-1.0 / 3.0,
    b2=0.0, b3=2.0 / 3.0,
    start_angle=0.5
)

layout_flat = Orientation(
    f0=3.0 / 2.0, f1=0.0,
    f2=math.sqrt(3.0) / 2.0, f3=math.sqrt(3.0),
    b0=2.0 / 3.0, b1=0.0,
    b2=-1.0 / 3.0, b3=math.sqrt(3.0) / 3.0,
    start_angle=0.0
)

class Hex:
    """
    Класс, представляющий шестиугольник с кубическими координатами (q, r, s).
    Он обеспечивает арифметические операции (сложение, вычитание, масштабирование),
    повороты, получение соседей, вычисление расстояния, интерполяцию,
    построение прямой и преобразования для отрисовки.
    """
    def __init__(self, q: float, r: float, s: float, terrain: Optional[str] = None):
        """
        Создаёт шестиугольник с координатами (q, r, s).
        Проверяет, что q + r + s == 0 (округляя результат).
        """
        if round(q + r + s) != 0:
            raise ValueError(
                f"Кубические координаты должны удовлетворять q + r + s = 0, получено: "
                f"q={q}, r={r}, s={s}"
            )
        self.q = q
        self.r = r
        self.s = s
        self.terrain = terrain

    def __repr__(self) -> str:
        return f"Hex(q={self.q}, r={self.r}, s={self.s}, terrain={self.terrain})"

    # Арифметические операции

    def __add__(self, other: Hex) -> Hex:
        """Возвращает новый Hex как сумму текущего и другого (компонентное сложение)."""
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s, terrain=self.terrain)

    def __sub__(self, other: Hex) -> Hex:
        """Возвращает новый Hex как разность текущего и другого (компонентное вычитание)."""
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s, terrain=self.terrain)

    def scale(self, k: float) -> Hex:
        """Масштабирует координаты Hex на коэффициент k."""
        return Hex(self.q * k, self.r * k, self.s * k, terrain=self.terrain)

    def rotate_left(self) -> Hex:
        """Поворачивает Hex на 60 градусов против часовой стрелки."""
        return Hex(-self.s, -self.q, -self.r, terrain=self.terrain)

    def rotate_right(self) -> Hex:
        """Поворачивает Hex на 60 градусов по часовой стрелке."""
        return Hex(-self.r, -self.s, -self.q, terrain=self.terrain)

    @staticmethod
    def direction(direction: int) -> Hex:
        """
        Возвращает базовый вектор направления (от 0 до 5) для получения соседа.
        """
        directions = [
            Hex(1, 0, -1),
            Hex(1, -1, 0),
            Hex(0, -1, 1),
            Hex(-1, 0, 1),
            Hex(-1, 1, 0),
            Hex(0, 1, -1)
        ]
        return directions[direction % 6]

    def neighbor(self, direction: int) -> Hex:
        """
        Возвращает соседний Hex в заданном направлении (от 0 до 5).
        """
        return self + Hex.direction(direction)

    @staticmethod
    def diagonal_direction(direction: int) -> Hex:
        """
        Возвращает базовый вектор для диагонального соседа (от 0 до 5).
        """
        diagonals = [
            Hex(2, -1, -1),
            Hex(1, -2, 1),
            Hex(-1, -1, 2),
            Hex(-2, 1, 1),
            Hex(-1, 2, -1),
            Hex(1, 1, -2)
        ]
        return diagonals[direction % 6]

    def diagonal_neighbor(self, direction: int) -> Hex:
        """
        Возвращает диагонального соседа в заданном направлении.
        """
        return self + Hex.diagonal_direction(direction)

    # Методы для вычисления расстояния и интерполяции

    def length(self) -> float:
        """
        Возвращает расстояние от центра (0, 0, 0) до этого Hex.
        """
        return (abs(self.q) + abs(self.r) + abs(self.s)) / 2

    def distance(self, other: Hex) -> float:
        """
        Возвращает расстояние между текущим Hex и другим Hex.
        """
        return (self - other).length()

    @staticmethod
    def lerp(a: Hex, b: Hex, t: float) -> Hex:
        """
        Линейно интерполирует между двумя Hex.
        
        :param a: начальный Hex
        :param b: конечный Hex
        :param t: параметр интерполяции от 0 (начало) до 1 (конец)
        :return: интерполированный Hex (в виде вещественных координат)
        """
        return Hex(
            a.q * (1.0 - t) + b.q * t,
            a.r * (1.0 - t) + b.r * t,
            a.s * (1.0 - t) + b.s * t,
            terrain=a.terrain
        )

    @staticmethod
    def round(h: Hex) -> Hex:
        """
        Округляет вещественные координаты Hex до целочисленных с сохранением условия q + r + s = 0.
        """
        qi = round(h.q)
        ri = round(h.r)
        si = round(h.s)

        q_diff = abs(qi - h.q)
        r_diff = abs(ri - h.r)
        s_diff = abs(si - h.s)

        if q_diff > r_diff and q_diff > s_diff:
            qi = -ri - si
        elif r_diff > s_diff:
            ri = -qi - si
        else:
            si = -qi - ri

        return Hex(qi, ri, si, terrain=h.terrain)

    @staticmethod
    def linedraw(a: Hex, b: Hex) -> List[Hex]:
        """
        Строит линию между двумя Hex в виде списка Hex, которые приближают прямую линию между ними.
        """
        N = int(a.distance(b))
        results = []
        # Небольшое смещение для избежания проблем округления:
        a_nudge = Hex(a.q + 1e-6, a.r + 1e-6, a.s - 2e-6, terrain=a.terrain)
        b_nudge = Hex(b.q + 1e-6, b.r + 1e-6, b.s - 2e-6, terrain=b.terrain)
        step = 1.0 / max(N, 1)
        for i in range(N + 1):
            interp_hex = Hex.lerp(a_nudge, b_nudge, step * i)
            results.append(Hex.round(interp_hex))
        return results

    # Методы для преобразования в пиксельные координаты (для отрисовки)

    def to_pixel(self, layout: Layout) -> Point:
        """
        Преобразует кубические координаты Hex в пиксельные координаты с использованием макета.
        :param layout: объект Layout, содержащий ориентацию, размер и начало координат.
        :return: точка (x, y) в пиксельных координатах
        """
        M = layout.orientation
        x = (M.f0 * self.q + M.f1 * self.r) * layout.size.x
        y = (M.f2 * self.q + M.f3 * self.r) * layout.size.y
        return Point(x + layout.origin.x, y + layout.origin.y)

    def polygon_corners(self, layout: Layout) -> List[Point]:
        """
        Вычисляет список вершин (углы) этого Hex для отрисовки.
        :param layout: объект Layout, содержащий ориентацию, размер и начало координат.
        :return: список точек, представляющих вершины шестигранника
        """
        center = self.to_pixel(layout)
        corners: List[Point] = []
        for i in range(6):
            # Вычисляем угол для данного угла шестиугольника
            angle = 2.0 * math.pi * (layout.orientation.start_angle - i) / 6.0
            offset = Point(layout.size.x * math.cos(angle), layout.size.y * math.sin(angle))
            corners.append(Point(center.x + offset.x, center.y + offset.y))
        return corners
    # В конец файла src/utils/hex_utils.py

    def hex_add(a: Hex, b: Hex) -> Hex:
        """
        Выполняет сложение двух hex, используя перегруженный оператор +.
        """
        return a + b

    def hex_direction(direction: int) -> Hex:
        """
        Возвращает базовый вектор направления для hex.
        """
        return Hex.direction(direction)
