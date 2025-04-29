import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Paddle class
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - 30
        self.speed = 10

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

# Ball class
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.x_speed = random.choice([-5, 5])
        self.y_speed = -5

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.x_speed *= -1

        if self.y <= 0:
            self.y_speed *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

# Brick class
class Brick:
    def __init__(self, x, y):
        self.width = 60
        self.height = 20
        self.x = x
        self.y = y
        self.color = BLUE
        self.is_visible = True

    def draw(self, screen):
        if self.is_visible:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Brick Breaker')
        self.clock = pygame.time.Clock()
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(x * 70 + 35, y * 30 + 35) for x in range(10) for y in range(5)]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move_left()
            if keys[pygame.K_RIGHT]:
                self.paddle.move_right()

            self.ball.move()

            # Ball collision with paddle
            if (self.paddle.y <= self.ball.y + self.ball.radius <= self.paddle.y + self.paddle.height) and (self.paddle.x <= self.ball.x <= self.paddle.x + self.paddle.width):
                self.ball.y_speed *= -1

            # Ball collision with bricks
            for brick in self.bricks:
                if brick.is_visible and (brick.y <= self.ball.y <= brick.y + brick.height) and (brick.x <= self.ball.x <= brick.x + brick.width):
                    self.ball.y_speed *= -1
                    brick.is_visible = False

            # Ball falls below screen
            if self.ball.y > SCREEN_HEIGHT:
                running = False

            self.screen.fill(BLACK)
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    Game().run()
