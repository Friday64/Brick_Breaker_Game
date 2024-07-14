import pygame
import sys
import random
import threading
import settings
from objects import Ball, Paddle, Brick
from powerups import generate_powerups, handle_powerups
from utils import draw_score, draw_tries, draw_level, draw_edges, detect_collisions

def start_game():
    """Start the game."""
    pygame.init()
    screen = pygame.display.set_mode((settings.width, settings.height), pygame.DOUBLEBUF | pygame.HWSURFACE)
    clock = pygame.time.Clock()

    paddle = Paddle(settings.width // 2 - settings.paddle_width // 2, settings.height - 200, settings.paddle_width, settings.paddle_height)
    ball = Ball(paddle.rect.centerx, paddle.rect.top - settings.ball_radius, settings.ball_radius)
    bricks = generate_bricks()
    powerups = []

    score = 0
    tries = 3
    current_level = 1
    running = True

    powerup_thread = threading.Thread(target=move_powerups, args=(powerups,))
    collision_thread = threading.Thread(target=detect_collisions, args=(ball, bricks, paddle, powerups))
    powerup_thread.start()
    collision_thread.start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        paddle.move(keys)
        ball.move()

        if ball.rect.bottom > settings.height:
            tries -= 1
            if tries <= 0:
                game_over_screen(screen, score)
                return
            ball.reset(paddle)

        screen.fill((0, 0, 0))
        draw_score(screen, score)
        draw_tries(screen, tries)
        draw_level(screen, current_level)
        draw_edges(screen)

        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)

        handle_powerups(powerups, paddle, [ball])

        pygame.display.flip()
        clock.tick(settings.frame_rate)

    pygame.quit()
    sys.exit()

def game_over_screen(screen, score):
    """Display the game over screen."""
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 50)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press Enter to Restart", True, (255, 255, 255))

    screen.blit(game_over_text, (settings.width // 2 - game_over_text.get_width() // 2, settings.height // 2 - 100))
    screen.blit(score_text, (settings.width // 2 - score_text.get_width() // 2, settings.height // 2))
    screen.blit(restart_text, (settings.width // 2 - restart_text.get_width() // 2, settings.height // 2 + 100))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

    start_game()

def generate_bricks():
    bricks = []
    brick_width = 100
    brick_height = 50
    brick_spacing = 10
    for i in range(5):  # 5 rows
        for j in range(10):  # 10 columns
            x = j * (brick_width + brick_spacing) + brick_spacing
            y = i * (brick_height + brick_spacing) + brick_spacing + 50
            bricks.append(Brick(x, y, brick_width, brick_height))
    return bricks

def move_powerups(powerups):
    while True:
        for powerup in powerups:
            powerup.move()
        pygame.time.wait(10)