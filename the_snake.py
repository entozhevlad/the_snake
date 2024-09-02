from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self, position):
        """Инициализация объекта с заданной позицией."""
        self.position = position


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализация яблока и установка случайной позиции."""
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Установка яблока в случайную позицию на поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        """Инициализация змейки с начальной позицией и направлением."""
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, grow=False):
        """Перемещение змейки в текущем направлении.

        Если параметр `grow` равен True, змейка увеличивается на один сегмент.
        """
        head_x, head_y = self.positions[0]
        new_head = (
            head_x + self.direction[0] * GRID_SIZE,
            head_y + self.direction[1] * GRID_SIZE
        )

        # Оборачиваем змейку при выходе за границы поля:
        new_head = (
            new_head[0] % SCREEN_WIDTH,
            new_head[1] % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if not grow:
            self.last = self.positions.pop()

    def check_self_collision(self):
        """Проверка на столкновение змейки с самой собой."""
        return self.positions[0] in self.positions[1:]

    def reset(self):
        """Сброс состояния змейки к начальному."""
        self.__init__()

    def draw(self):
        """Отрисовка змейки на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки:
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента:
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработка ввода с клавиатуры для изменения направления змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция, запускающая игру."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        if snake.positions[0] == apple.position:
            snake.move(grow=True)
            apple.randomize_position()
        else:
            snake.move(grow=False)

        if snake.check_self_collision():
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
