import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение констант
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
SNAKE_SIZE = 20
INITIAL_SPEED = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Определение класса для змейки
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, dir):
        if self.length > 1 and (dir[0] * -1, dir[1] * -1) == self.direction:
            return
        else:
            self.direction = dir

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

# Определение класса для еды
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, SCREEN_WIDTH / GRID_SIZE - 1) * GRID_SIZE,
                         random.randint(0, SCREEN_HEIGHT / GRID_SIZE - 1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)

# Функция для обработки столкновений
def collision_with_boundaries(snake):
    return (snake.get_head_position()[0] in (0, SCREEN_WIDTH - GRID_SIZE) or
            snake.get_head_position()[1] in (0, SCREEN_HEIGHT - GRID_SIZE))

def collision_with_self(snake):
    return snake.get_head_position() in snake.positions[1:]

# Основная функция игры
def main():
    # Создание окна
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')

    # Инициализация переменных
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    speed = INITIAL_SPEED

    # Основной игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.turn((1, 0))

        # Движение змейки
        snake.move()

        # Проверка столкновений
        if collision_with_boundaries(snake) or collision_with_self(snake):
            snake.reset()
            speed = INITIAL_SPEED

        # Проверка съедания еды
        if snake.get_head_position() == food.position:
            snake.length += 1
            speed += 1
            food.randomize_position()

        # Отрисовка экрана
        screen.fill(WHITE)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.update()
        clock.tick(speed)


# Запуск игры
if __name__ == "__main__":
    main()



