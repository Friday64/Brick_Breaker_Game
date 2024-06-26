import pygame
import pygame_menu
import sys
import random
import math
import settings

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
screen = pygame.display.set_mode((settings.width, settings.height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Brick Breaker")

# Colors for the game text
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Frame rate setup
frame_rate = settings.frame_rate  # Adjustable frame rate

# Paddle settings
paddle_width = settings.paddle_width
paddle_height = settings.paddle_height
paddle_pos_y = settings.height - 200
paddle_pos_x = settings.width // 2 - settings.paddle_width // 2
paddle_speed = settings.paddle_speed

# Level settings
current_level = 1

# Multiball settings
multiball_active = False
multiball_powerup = None

# Global variables for ball settings
ball_radius = settings.ball_radius
ball_color = BLUE
ball_pos = [settings.width // 2, settings.height // 2]
angle = random.uniform(30, 150)
speed = random.uniform(7, 13)
velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]

# List to keep track of all active balls
balls = [{"pos": ball_pos, "velocity": velocity}]

# Function to generate random colors
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Brick settings
brick_rows = 5
brick_columns = 10
brick_width = 100
brick_height = 50
brick_spacing = 10
brick_offset_x = (settings.width - (brick_columns * (brick_width + brick_spacing))) // 2
brick_offset_y = 50

# Generate bricks
def generate_bricks(level):
    bricks = []
    for i in range(brick_rows):
        row = []
        for j in range(brick_columns):
            if random.random() < 0.5:  # Randomly decide whether to place a brick
                brick_rect = pygame.Rect(brick_offset_x + j * (brick_width + brick_spacing),
                                         brick_offset_y + i * (brick_height + brick_spacing),
                                         brick_width, brick_height)
                row.append({"rect": brick_rect, "color": random_color()})
            else:
                row.append(None)  # No brick in this position
        bricks.append(row)
    return bricks

# Function to generate a multiball power-up
def generate_multiball_powerup():
    x = random.randint(100, settings.width - 100)
    y = 0  # Start at the top of the screen
    return {"rect": pygame.Rect(x, y, 30, 30), "color": GREEN, "speed": 5}

# Function to draw edges of the screen
def draw_edges():
    edge_thickness = 10
    edge_color = (255, 255, 255, 128)  # White with transparency
    pygame.draw.rect(screen, edge_color, (0, 0, edge_thickness, settings.height), 0)
    pygame.draw.rect(screen, edge_color, (settings.width - edge_thickness, 0, edge_thickness, settings.height), 0)
    pygame.draw.rect(screen, edge_color, (0, 0, settings.width, edge_thickness), 0)
    pygame.draw.rect(screen, edge_color, (0, settings.height - edge_thickness, settings.width, edge_thickness), 0)

# Function to draw number of tries on the right-hand side of the screen while the game is running
def draw_tries(tries):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Tries: " + str(tries), True, WHITE)
    screen.blit(text, (settings.width - 300, 20))

# Function to draw the score on the left-hand side of the screen
def draw_score(score):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (20, 20))

# Function to draw the current level at the bottom right of the screen
def draw_level(level):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Level: " + str(level), True, WHITE)
    text_rect = text.get_rect(bottomright=(settings.width - 20, settings.height - 20))
    screen.blit(text, text_rect)

# Function to draw bricks
def draw_bricks(bricks):
    for row in bricks:
        for brick in row:
            if brick:  # Only draw if there is a brick
                pygame.draw.rect(screen, brick["color"], brick["rect"])

# Function to draw the paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, paddle_width, paddle_height), 0)

# Function to draw the multiball power-up
def draw_multiball_powerup(powerup):
    if powerup:
        pygame.draw.rect(screen, powerup["color"], powerup["rect"])

# Function to move the paddle
def move_paddle():
    global paddle_pos_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        paddle_pos_x -= paddle_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        paddle_pos_x += paddle_speed

    # Make sure the paddle doesn't go off screen
    if paddle_pos_x < 0:
        paddle_pos_x = 0
    if paddle_pos_x > settings.width - paddle_width:
        paddle_pos_x = settings.width - paddle_width

def ball_behavior():
    global running, tries, score, current_level, bricks, multiball_active, balls, multiball_powerup

    for ball in balls:
        ball_pos = ball["pos"]
        velocity = ball["velocity"]

        # Bounce off the left and right edges
        if ball_pos[0] - ball_radius <= 0:
            ball_pos[0] = ball_radius
            velocity[0] = -velocity[0]
        elif ball_pos[0] + ball_radius >= settings.width:
            ball_pos[0] = settings.width - ball_radius
            velocity[0] = -velocity[0]

        # Bounce off the top edge
        if ball_pos[1] - ball_radius <= 0:
            ball_pos[1] = ball_radius
            velocity[1] = -velocity[1]

        # Ball falls below the bottom edge
        if ball_pos[1] + ball_radius >= settings.height:
            balls.remove(ball)

        # Ball collision detection with paddle
        if (paddle_pos_x <= ball_pos[0] <= paddle_pos_x + paddle_width and
                paddle_pos_y - ball_radius <= ball_pos[1] <= paddle_pos_y):
            velocity[1] = -velocity[1]
            ball_pos[1] = paddle_pos_y - ball_radius  # Ensures the ball doesn't get stuck in the paddle

        # Ball collision detection with bricks
        for row in bricks:
            for brick in row:
                if brick and brick["rect"].colliderect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, 2 * ball_radius, 2 * ball_radius):
                    row.remove(brick)
                    score += 10
                    velocity[1] = -velocity[1]
                    break

        # Update ball position
        ball_pos[0] += velocity[0]
        ball_pos[1] += velocity[1]

    # Check for all balls out of bounds
    if len(balls) == 0:
        if tries > 0:
            # Reset ball position
            ball_pos = [settings.width // 2, settings.height // 2]
            angle = random.uniform(30, 150)
            speed = random.uniform(7, 11)
            velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]
            balls.append({"pos": ball_pos, "velocity": velocity})

            # Decrease the number of tries
            tries -= 1
        elif tries == 0:
            running = False
            # Display game over screen
            game_over_screen()

    # Move the power-up down the screen
    if multiball_powerup:
        multiball_powerup["rect"].y += multiball_powerup["speed"]

    # Check for collision with multiball power-up
    if multiball_powerup and multiball_powerup["rect"].colliderect(paddle_pos_x, paddle_pos_y, paddle_width, paddle_height):
        multiball_active = True
        multiball_powerup = None
        for _ in range(2):  # Add two more balls
            angle = random.uniform(30, 150)
            speed = random.uniform(7, 13)
            new_velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]
            balls.append({"pos": ball_pos.copy(), "velocity": new_velocity})

    # Check if all bricks are cleared
    if all(all(brick is None for brick in row) for row in bricks):
        # Advance to the next level
        current_level += 1
        if current_level > settings.num_levels:
            current_level = 1  # Restart at level 1
        bricks = generate_bricks(current_level)
        multiball_active = False
        ball_pos = [settings.width // 2, settings.height // 2]
        angle = random.uniform(30, 150)
        speed = random.uniform(7, 13)
        velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]
        balls = [{"pos": ball_pos, "velocity": velocity}]

def game_over_screen():
    screen.fill(BLACK)
    
    font = pygame.font.SysFont(None, 50)
    texts = ["Game Over", f"Score: {score}", "Press Enter to Restart"]
    y_offset = settings.height // 2 - 100  # Start a bit higher on the screen

    for text in texts:
        rendered_text = font.render(text, True, WHITE)
        text_rect = rendered_text.get_rect(center=(settings.width // 2, y_offset))
        screen.blit(rendered_text, text_rect)
        y_offset += 100  # Move down for the next line of text

    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
                start_game()

def start_game():
    global running, tries, score, ball_pos, velocity, bricks, current_level, multiball_active, multiball_powerup, balls, angle, speed

    # Reset tries, score, level, and ball position
    tries = 3
    score = 0
    current_level = 1
    ball_pos = [settings.width // 2, settings.height // 2]
    angle = random.uniform(30, 150)
    speed = random.uniform(7, 13)
    velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]
    balls = [{"pos": ball_pos, "velocity": velocity}]

    # Generate bricks for the first level
    bricks = generate_bricks(current_level)
    multiball_active = False
    multiball_powerup = None

    running = True

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw_score(score)
        draw_tries(tries)
        draw_level(current_level)
        draw_paddle(paddle_pos_x, paddle_pos_y)
        move_paddle()
        draw_bricks(bricks)
        draw_edges()
        if not multiball_active and random.random() < 0.001:  # Low probability to generate power-up
            multiball_powerup = generate_multiball_powerup()
        draw_multiball_powerup(multiball_powerup)
        ball_behavior()

        for ball in balls:
            pygame.draw.circle(screen, ball_color, (int(ball["pos"][0]), int(ball["pos"][1])), ball_radius)
        
        pygame.display.flip()
        pygame.time.Clock().tick(frame_rate)

    # Quit Pygame
    pygame.quit()
    sys.exit()

def menu():
    menu = pygame_menu.Menu('Brick Breaker', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

if __name__ == "__main__":
    menu()
