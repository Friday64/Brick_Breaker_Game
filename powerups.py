import random
import pygame
import settings

class Powerup:
    def __init__(self, x, y, color, effect):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = color
        self.effect = effect
        self.speed = 5

    def move(self):
        self.rect.y += self.speed
        return self.rect.top <= settings.height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def generate_powerups():
    x = random.randint(100, settings.width - 100)
    powerup_types = {
        'multiball': (0, 255, 0),  # Green
        'paddle_size': (255, 255, 0),  # Yellow
        'slow_ball': (128, 0, 128)  # Purple
    }
    powerup_type = random.choice(list(powerup_types.keys()))
    return Powerup(x, 0, powerup_types[powerup_type], powerup_type)

def handle_powerups(powerups, paddle, balls):
    for powerup in powerups[:]:
        if powerup.rect.colliderect(paddle.rect):
            if powerup.effect == 'multiball':
                new_ball = balls[0].__class__(balls[0].rect.centerx, balls[0].rect.centery, settings.ball_radius)
                new_ball.attached = False
                new_ball.direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
                balls.append(new_ball)
            elif powerup.effect == 'paddle_size':
                paddle.rect.width *= 1.5
            elif powerup.effect == 'slow_ball':
                for ball in balls:
                    ball.speed *= 0.5
            powerups.remove(powerup)