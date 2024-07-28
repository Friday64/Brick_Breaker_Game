import pygame
import sys
import random
import settings
from objects import Ball, Paddle, Brick
from powerups import generate_powerup, handle_powerups
from utils import draw_score, draw_tries, draw_level, draw_edges

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((settings.width, settings.height))
    clock = pygame.time.Clock()

    paddle = Paddle(settings.width // 2 - settings.paddle_width // 2, settings.height - 50, settings.paddle_width, settings.paddle_height)
    ball = Ball(paddle.rect.centerx, paddle.rect.top - settings.ball_radius, settings.ball_radius)
    bricks = generate_bricks()
    powerups = []

    score = 0
    tries = 3
    current_level = 1
    running = True

    while running:
        running = handle_events(ball)
        update_game_state(paddle, ball, bricks, powerups, score, tries)
        draw_game(screen, paddle, ball, bricks, powerups, score, tries, current_level)
        pygame.display.flip()
        clock.tick(settings.frame_rate)

    pygame.quit()
    sys.exit()

def handle_events(ball):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print("Space pressed, detaching ball")
            ball.attached = False
            if ball.direction == [0, -1]:
                ball.direction = [random.choice([-1, 1]), -1]
    return True

def update_game_state(paddle, ball, bricks, powerups, score, tries):
    keys = pygame.key.get_pressed()
    paddle.move(keys)
    
    print(f"Before move - Ball pos: {ball.rect.center}, direction: {ball.direction}, speed: {ball.speed}, attached: {ball.attached}")
    ball.move()
    print(f"After move - Ball pos: {ball.rect.center}, direction: {ball.direction}, speed: {ball.speed}, attached: {ball.attached}")

    if ball.rect.bottom > settings.height:
        print("Ball out of bounds, resetting...")
        tries -= 1
        if tries <= 0:
            print("Game over")
            return
        ball.reset(paddle)
        print(f"After reset - Ball pos: {ball.rect.center}, direction: {ball.direction}, speed: {ball.speed}, attached: {ball.attached}")

    # Ball-Paddle collision
    if ball.rect.colliderect(paddle.rect) and ball.direction[1] > 0:
        ball.direction[1] *= -1
        ball.rect.bottom = paddle.rect.top

    # Ball-Brick collisions
    for brick in bricks[:]:
        if ball.rect.colliderect(brick.rect):
            ball.direction[1] *= -1
            bricks.remove(brick)
            score += 1
            if random.random() < 0.1:  # 10% chance to spawn a powerup
                powerups.append(generate_powerup())

    handle_powerups(powerups, paddle, [ball])

def draw_game(screen, paddle, ball, bricks, powerups, score, tries, current_level):
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

def generate_bricks():
    bricks = []
    brick_width, brick_height = 60, 20
    brick_spacing = 10
    for i in range(5):
        for j in range(10):
            x = j * (brick_width + brick_spacing) + brick_spacing
            y = i * (brick_height + brick_spacing) + brick_spacing + 50
            bricks.append(Brick(x, y, brick_width, brick_height))
    return bricks