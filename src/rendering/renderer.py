# src/rendering/renderer.py

import pygame
from src.utils.hex_utils import Hex as HexUtils   # Импортируем новый класс Hex
from src.utils.helpers import hex_to_pixel, layout, get_hex_corners, pixel_to_hex, Point

class Renderer:
    def __init__(self, grid, screen_width=800, screen_height=600, hex_size=30):
        self.grid = grid
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.hex_size = hex_size

        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Hex Grid Game")
        self.running = True
        self.clock = pygame.time.Clock()

        # Цвета для типов местности
        self.terrain_colors = {
            "grass": (0, 128, 0),  # Зеленый
            "water": (0, 0, 255),  # Синий
            None: (200, 200, 200)  # Серый для неопределенной местности
        }

        # Цвет для выделенного шестиугольника
        self.highlight_color = (255, 255, 0)  # Желтый

        # Текущий выделенный шестиугольник (q, r, s) или None, если ничего не выбрано
        self.selected_hex = None

        # Флаг для отображения координат
        self.show_coordinates = False

        # Шрифт для отображения текста
        self.font = pygame.font.SysFont(None, 36)

        # Анимация
        self.animation_steps = []           # Список шагов анимации [(q, r, s), ...]
        self.animation_speed = 10           # Количество кадров для анимации (меньше = быстрее)
        self.animation_counter = 0          # Счётчик кадров анимации
        self.current_animation_hex = None   # Текущая позиция в анимации

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Обработка клика мыши
                    self.handle_mouse_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    # Обработка нажатия клавиш
                    self.handle_key_press(event.key)

            # Обновляем анимацию, если она активна
            if self.animation_steps:
                self.update_animation()

            # Очистка экрана
            self.screen.fill((255, 255, 255))  # Белый фон

            # Отрисовка сетки
            self.draw_grid()

            # Отрисовка координат, если включено
            if self.show_coordinates and self.selected_hex is not None:
                self.draw_coordinates()

            # Обновление экрана
            pygame.display.flip()
            self.clock.tick(60)  # Ограничиваем FPS

        # Очистка
        pygame.quit()

    def handle_mouse_click(self, pos):
        """
        Обработка клика мыши в заданной позиции (x, y).
        Преобразует позицию в шестиугольные координаты и выделяет шестиугольник, если он существует.
        """
        offset_x = self.screen_width // 2
        offset_y = self.screen_height // 2
        x, y = pos
        x -= offset_x
        y -= offset_y

        # Преобразуем пиксельные координаты в кубические координаты
        hex_obj = pixel_to_hex(layout, Point(x, y))
        q, r, s = hex_obj.q, hex_obj.r, hex_obj.s

        if self.grid.get_hex(q, r, s) is not None:
            self.selected_hex = (q, r, s)
            print(f"Выбран шестиугольник: (q={q}, r={r}, s={s})")
        else:
            self.selected_hex = None

    def handle_key_press(self, key):
        """
        Обработка нажатия клавиш для перемещения выделения и управления отображением координат.
        """
        # Переключение отображения координат (клавиша C)
        if key == pygame.K_c:
            self.show_coordinates = not self.show_coordinates
            return

        # Если анимация активна, игнорируем новые нажатия
        if self.animation_steps:
            return

        # Если ничего не выбрано, выбираем центральный шестиугольник (0, 0, 0)
        if self.selected_hex is None:
            if self.grid.get_hex(0, 0, 0) is not None:
                self.selected_hex = (0, 0, 0)
            return

        # Получаем текущие координаты
        q, r, s = self.selected_hex

        # Направления в кубических координатах
        directions = {
            pygame.K_d: (1, 0, -1),   # Вправо
            pygame.K_a: (-1, 0, 1),   # Влево
            pygame.K_w: (0, -1, 1),   # Вверх
            pygame.K_s: (0, 1, -1),   # Вниз
            pygame.K_q: (1, -1, 0),   # Вверх-вправо
            pygame.K_e: (-1, 1, 0)    # Вниз-влево
        }

        # Проверяем, соответствует ли нажатая клавиша одному из направлений
        if key in directions:
            dq, dr, ds = directions[key]
            new_q, new_r, new_s = q + dq, r + dr, s + ds

            # Оборачиваем координаты, передавая направление движения
            final_q, final_r, final_s = self.grid.wrap_coordinates(new_q, new_r, new_s, direction=(dq, dr, ds))

            # Если произошло оборачивание, создаём анимацию
            if (new_q, new_r, new_s) != (final_q, final_r, final_s) and max(abs(new_q), abs(new_r), abs(new_s)) > self.grid.radius:
                self.animation_steps = [(q, r, s), (new_q, new_r, new_s), (final_q, final_r, final_s)]
                self.animation_counter = 0
                self.current_animation_hex = (q, r, s)
            else:
                # Если оборачивания нет, просто перемещаем выделение
                self.selected_hex = (final_q, final_r, final_s)

    def update_animation(self):
        """
        Обновляет состояние анимации.
        """
        if not self.animation_steps:
            return

        self.animation_counter += 1

        # Вычисляем текущий шаг анимации
        total_steps = len(self.animation_steps) - 1
        step_duration = self.animation_speed
        current_segment = self.animation_counter // step_duration
        progress = (self.animation_counter % step_duration) / step_duration

        if current_segment >= total_steps:
            # Анимация завершена
            final_q, final_r, final_s = self.animation_steps[-1]
            self.selected_hex = (final_q, final_r, final_s)
            self.animation_steps = []
            self.current_animation_hex = None
            return

        # Интерполируем с использованием Hex.lerp
        start_q, start_r, start_s = self.animation_steps[current_segment]
        end_q, end_r, end_s = self.animation_steps[current_segment + 1]
        start_hex = HexUtils(start_q, start_r, start_s)
        end_hex = HexUtils(end_q, end_r, end_s)

        interpolated_hex = HexUtils.lerp(start_hex, end_hex, progress)
        rounded_hex = HexUtils.round(interpolated_hex)
        self.current_animation_hex = (rounded_hex.q, rounded_hex.r, rounded_hex.s)

    def draw_grid(self):
        offset_x = self.screen_width // 2
        offset_y = self.screen_height // 2

        # Отрисовка всех шестиугольников
        for hex_obj in self.grid.hexes.values():
            # Проверяем, что q + r + s == 0
            if round(hex_obj.q + hex_obj.r + hex_obj.s) != 0:
                continue

            # hex_obj уже является объектом типа Hex
            pixel = hex_to_pixel(layout, hex_obj)
            x = pixel.x + offset_x
            y = pixel.y + offset_y
            corners = get_hex_corners(hex_obj.q, hex_obj.r, hex_obj.s)

            if not corners:
                continue

            adjusted_corners = [(corner.x + offset_x, corner.y + offset_y) for corner in corners]

            if self.selected_hex and (hex_obj.q, hex_obj.r, hex_obj.s) == self.selected_hex and not self.animation_steps:
                color = self.highlight_color
            else:
                color = self.terrain_colors.get(hex_obj.terrain, self.terrain_colors[None])

            pygame.draw.polygon(self.screen, color, adjusted_corners)
            pygame.draw.polygon(self.screen, (0, 0, 0), adjusted_corners, 1)

        # Отрисовка анимированного шестиугольника
        if self.current_animation_hex:
            q, r, s = self.current_animation_hex
            if round(q + r + s) != 0:
                return

            pixel = hex_to_pixel(layout, HexUtils(q, r, s))
            x = pixel.x + offset_x
            y = pixel.y + offset_y
            corners = get_hex_corners(q, r, s)

            if not corners:
                return

            adjusted_corners = [(corner.x + offset_x, corner.y + offset_y) for corner in corners]
            pygame.draw.polygon(self.screen, self.highlight_color, adjusted_corners)
            pygame.draw.polygon(self.screen, (0, 0, 0), adjusted_corners, 1)

    def draw_coordinates(self):
        """
        Отображает координаты текущего выделенного шестиугольника на экране.
        """
        if self.selected_hex is None:
            return

        q, r, s = self.selected_hex
        text = f"q: {q}, r: {r}, s: {s}"
        text_surface = self.font.render(text, True, (0, 0, 0))  # Черный текст
        self.screen.blit(text_surface, (10, 10))
