import random
import pygame
import settings

class Powerup:
    def __init__(self, x, y, color, effect):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.effect = effect
        self.speed = 2

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

def generate_powerup():
    x = random.randint(0, settings.width - 20)
    powerup_type = random.choice(['multiball', 'paddle_size', 'slow_ball'])
    if powerup_type == 'multiball':
        return Powerup(x, 0, (0, 255, 0), 'multiball')  # Green
    elif powerup_type == 'paddle_size':
        return Powerup(x, 0, (255, 255, 0), 'paddle_size')  # Yellow
    else:
        return Powerup(x, 0, (128, 0, 128), 'slow_ball')  # Purple

def handle_powerups(powerups, paddle, balls):
    for powerup in powerups[:]:
        powerup.move()
        if powerup.rect.colliderect(paddle.rect):
            if powerup.effect == 'multiball':
                new_ball = Ball(balls[0].rect.centerx, balls[0].rect.centery, settings.ball_radius)
                new_ball.attached = False
                new_ball.direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
                balls.append(new_ball)
            elif powerup.effect == 'paddle_size':
                paddle.rect.width = min(paddle.rect.width * 1.5, settings.width)
            elif powerup.effect == 'slow_ball':
                for ball in balls:
                    ball.speed = max(ball.speed * 0.5, 1)
            powerups.remove(powerup)
        elif powerup.rect.top > settings.height:
            powerups.remove(powerup)