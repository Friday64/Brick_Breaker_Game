import pygame
import settings
import random

generate_powerups = lambda: random.randint(0, 2)
handle_powerups = lambda: None
def draw_score(screen, score):
    font = pygame.font.SysFont(None, 50)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (20, 20))

def draw_tries(screen, tries):
    font = pygame.font.SysFont(None, 50)
    text = font.render(f"Tries: {tries}", True, (255, 255, 255))
    screen.blit(text, (settings.width - 300, 20))

def draw_level(screen, level):
    font = pygame.font.SysFont(None, 50)
    text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(text, (settings.width - 300, settings.height - 50))

def draw_edges(screen):
    edge_thickness = 10
    edge_color = (255, 255, 255, 128)  # White with transparency
    pygame.draw.rect(screen, edge_color, (0, 0, edge_thickness, settings.height))
    pygame.draw.rect(screen, edge_color, (settings.width - edge_thickness, 0, edge_thickness, settings.height))
    pygame.draw.rect(screen, edge_color, (0, 0, settings.width, edge_thickness))

def detect_collisions(ball, bricks, paddle, powerups):
    # Ball-Paddle collision
    if ball.rect.colliderect(paddle.rect) and ball.direction[1] > 0:
        ball.direction[1] *= -1
        ball.rect.bottom = paddle.rect.top

    # Ball-Brick collisions
    for brick in bricks:
        if ball.rect.colliderect(brick.rect):
            ball.direction[1] *= -1
            bricks.remove(brick)
            if random.random() < 0.1:  # 10% chance to spawn a powerup
                powerups.append(generate_powerups())

    # Powerup-Paddle collisions
    for powerup in powerups:
        if powerup.rect.colliderect(paddle.rect):
            handle_powerups([powerup], paddle, [ball])
            powerups.remove(powerup)