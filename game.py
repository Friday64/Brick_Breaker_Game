import pygame
import sys
import random
import settings
from objects import Ball, Paddle, Brick
from powerups import generate_powerup, handle_powerups
from utils import draw_score, draw_tries, draw_level, draw_edges


def start_game():
    """
    Initializes the game, sets up the screen, and enters the main game loop.

    This function initializes the Pygame library and creates a screen of the specified width and height.
    It then creates a paddle, a ball, a list of bricks, an empty list of powerups, and sets the initial score,
    tries, and current level to 0, 3, and 1 respectively.

    The main game loop continues as long as the running variable is True. It first checks for any events
    (e.g. keyboard presses, mouse clicks) using the handle_events function. Then it updates the game state
    by calling the update_game_state function with the paddle, ball, bricks, powerups, score, and tries as
    arguments. After that, it draws the game on the screen using the draw_game function. Finally, it flips the
    display and updates the clock to maintain the desired frame rate.

    If the running variable becomes False, the game loop is exited and the Pygame library is quit, and the
    program terminates.

    This function does not take any parameters and does not return any values.
    """
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
    """
    Handle events in the game.

    Parameters:
        ball (Ball): The ball object.

    Returns:
        bool: True if the game should continue, False if the game should end.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ball.attached = False
    return True

def update_game_state(paddle, ball, bricks, powerups, score, tries):
    """
    Update the game state.

    Parameters:
        paddle (Paddle): The paddle object.
        ball (Ball): The ball object.
        bricks (list): A list of Brick objects.
        powerups (list): A list of Powerup objects.
        score (int): The current score.
        tries (int): The number of tries remaining.

    Returns:
        None
    """
    keys = pygame.key.get_pressed()
    paddle.move(keys)
    ball.move(bricks)
    if ball.rect.bottom > settings.height:
        print("Ball out of bounds, resetting...")
        tries -= 1
        if tries <= 0:
            print("Game over")
            return
        ball.reset(paddle)
    

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
    """
    Draws the game on the screen.

    Args:
        screen (pygame.Surface): The surface to draw on.
        paddle (Paddle): The paddle object.
        ball (Ball): The ball object.
        bricks (list): A list of Brick objects.
        powerups (list): A list of Powerup objects.
        score (int): The current score.
        tries (int): The number of tries remaining.
        current_level (int): The current level.

    Returns:
        None
    """
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
    """
    Generate a list of Brick objects.

    Returns:
        list: A list of Brick objects.
    """
    bricks = []
    brick_width, brick_height = 60, 20
    brick_spacing = 10
    for i in range(5):
        for j in range(10):
            x = j * (brick_width + brick_spacing) + brick_spacing
            y = i * (brick_height + brick_spacing) + brick_spacing + 50
            bricks.append(Brick(x, y, brick_width, brick_height))
    return bricks