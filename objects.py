import pygame
import random
import math
import settings

class Ball:
    def __init__(self, x, y, radius):
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.color = (0, 0, 255)  # Blue
        self.speed = random.uniform(7, 13)
        self.direction = [0, -1]  # Start moving upwards
        self.attached = True

    def move(self):
        if not self.attached:
            self.rect.move_ip(self.direction[0] * self.speed, self.direction[1] * self.speed)
            if self.rect.left <= 0 or self.rect.right >= settings.width:
                self.direction[0] *= -1
            if self.rect.top <= 0:
                self.direction[1] *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def reset(self, paddle):
        self.rect.midbottom = paddle.rect.midtop
        self.attached = True
        self.direction = [0, -1]

class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White
        self.speed = settings.paddle_speed

    def move(self, keys):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.rect.x = max(0, min(settings.width - self.rect.width, self.rect.x + dx))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)