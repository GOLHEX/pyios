# src/core/hex_grid.py

from src.utils.hex_utils import Hex  # Импортируем новый класс Hex

class HexGrid:
    def __init__(self):
        self.hexes = {}  # Ключ: (q, r, s), значение: Hex
        self.radius = 0

    def add_hex(self, hex_obj: Hex):
        self.hexes[(hex_obj.q, hex_obj.r, hex_obj.s)] = hex_obj

    def get_hex(self, q, r, s):
        return self.hexes.get((q, r, s))

    def generate_hexagonal_grid(self, radius: int):
        self.radius = radius
        self.hexes.clear()

        # Генерируем сетку
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                s = -q - r
                if max(abs(q), abs(r), abs(s)) <= radius:
                    print(f"Generating hex (q={q}, r={r}, s={s}), sum={q + r + s}")
                    hex_obj = Hex(q, r, s, terrain="grass")
                    self.add_hex(hex_obj)

    def get_neighbors(self, q, r, s):
        """
        Возвращает список соседних шестиугольников в кубических координатах.
        """
        neighbors = []
        # Создаем базовый Hex для заданных координат
        base_hex = Hex(q, r, s)
        for direction in range(6):  # 6 направлений
            # Используем перегруженный оператор + и статический метод direction
            neighbor = base_hex + Hex.direction(direction)
            # Если такой hex существует в сетке, добавляем его координаты
            if self.get_hex(neighbor.q, neighbor.r, neighbor.s) is not None:
                neighbors.append((neighbor.q, neighbor.r, neighbor.s))
        return neighbors

    def wrap_coordinates(self, q, r, s, direction=None):
        """
        "Оборачивает" координаты (q, r, s), если они выходят за пределы сетки.
        Возвращает новые координаты (q, r, s).
        """
        # Проверяем, находится ли точка внутри сетки
        if max(abs(q), abs(r), abs(s)) <= self.radius and self.get_hex(q, r, s) is not None:
            return q, r, s

        # Если передано направление, корректируем координаты
        if direction:
            dq, dr, ds = direction
            q += dq
            r += dr
            s += ds

        # Нормализуем координаты, чтобы они оставались в пределах радиуса
        while max(abs(q), abs(r), abs(s)) > self.radius:
            if q > self.radius:
                q -= 2 * self.radius + 1
                r += self.radius + 1
                s += self.radius + 1
            elif q < -self.radius:
                q += 2 * self.radius + 1
                r -= self.radius + 1
                s -= self.radius + 1

            if r > self.radius:
                r -= 2 * self.radius + 1
                q += self.radius + 1
                s += self.radius + 1
            elif r < -self.radius:
                r += 2 * self.radius + 1
                q -= self.radius + 1
                s -= self.radius + 1

            if s > self.radius:
                s -= 2 * self.radius + 1
                q += self.radius + 1
                r += self.radius + 1
            elif s < -self.radius:
                s += 2 * self.radius + 1
                q -= self.radius + 1
                r -= self.radius + 1

        # Проверяем, существует ли шестиугольник с новыми координатами
        if self.get_hex(q, r, s) is not None:
            return q, r, s

        # Если ничего не найдено, возвращаем центр сетки
        return 0, 0, 0