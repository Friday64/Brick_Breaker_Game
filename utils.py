import pygame
import settings
import random

def generate_powerups():
    return random.randint(0, 2)

def handle_powerups():
    pass

def draw_text(screen, text, position, font_size=50, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, font_size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)

def draw_score(screen, score):
    draw_text(screen, f"Score: {score}", (20, 20))

def draw_tries(screen, tries):
    draw_text(screen, f"Tries: {tries}", (settings.width - 300, 20))

def draw_level(screen, level):
    draw_text(screen, f"Level: {level}", (settings.width - 300, settings.height - 50))

def draw_edges(screen):
    edge_thickness = 10
    edge_color = (255, 255, 255, 128)  # White with transparency
    edges = [
        (0, 0, edge_thickness, settings.height),
        (settings.width - edge_thickness, 0, edge_thickness, settings.height),
        (0, 0, settings.width, edge_thickness)
    ]
    for edge in edges:
        pygame.draw.rect(screen, edge_color, edge)

def detect_collisions(ball, bricks, paddle, powerups):
    # Ball-Paddle collision
    if ball.rect.colliderect(paddle.rect) and ball.direction[1] > 0:
        ball.direction[1] *= -1
        ball.rect.bottom = paddle.rect.top

    # Ball-Brick collisions
    for brick in bricks[:]:  # Use a copy of the list to safely remove items
        if ball.rect.colliderect(brick.rect):
            ball.direction[1] *= -1
            bricks.remove(brick)
            if random.random() < 0.1:  # 10% chance to spawn a powerup
                powerups.append(generate_powerups())

    # Powerup-Paddle collisions
    for powerup in powerups[:]:  # Use a copy of the list to safely remove items
        if powerup.rect.colliderect(paddle.rect):
            handle_powerups([powerup], paddle, [ball])
            powerups.remove(powerup)