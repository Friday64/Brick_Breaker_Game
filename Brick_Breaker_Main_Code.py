import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Colors for the game text
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# add Countdown timer function on black screen for 5 seconds on game start when a button is pressed then clear screen
def countdown_timer():
  #display timer on black screen using fullscreen pygame text
  screen.fill(BLACK)
  font = pygame.font.SysFont(None, 48)
  text = font.render("3", 1, WHITE)
  screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
  
  #Display text saying "Game will start when any key is pressed" and then start 5 second countdown timer on screen when key is pressed
  pygame.display.flip()
  pygame.time.delay(5000)
  screen.fill(BLACK)
  text = font.render("Game will start in 5 seconds", 1, WHITE)
  screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
  pygame.display.flip()
  pygame.time.delay(5000)

  #clear screen
  screen.fill(BLACK)
  pygame.display.flip()

  #end function here
  return
 
  






# Screen dimensions and settings
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Brick Breaker")

# Fill the screen with black
screen.fill(BLACK)

# Edges of the screen
def draw_edges():
    pygame.draw.rect(screen, WHITE, (0, 0, 10, height), 0)
    pygame.draw.rect(screen, WHITE, (width - 10, 0, 10, height), 0)
    pygame.draw.rect(screen, WHITE, (0, 0, width, 10), 0)
    pygame.draw.rect(screen, WHITE, (0, height - 10, width, 10), 0)

# Paddle settings
paddle_width = 400
paddle_height = 20
paddle_pos_y = height - 200
paddle_pos_x = width // 2 - paddle_width // 2
paddle_speed = 10

# Function to generate random colors
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

# Brick settings
brick_rows = 5
brick_columns = 10
brick_width = 100
brick_height = 50
brick_spacing = 10
brick_offset_x = (width - (brick_columns * (brick_width + brick_spacing))) // 2
brick_offset_y = 50

# Generate bricks
bricks = []
for i in range(brick_rows):
    row = []
    for j in range(brick_columns):
        brick_rect = pygame.Rect(brick_offset_x + j * (brick_width + brick_spacing),
                                 brick_offset_y + i * (brick_height + brick_spacing),
                                 brick_width, brick_height)
        row.append({"rect": brick_rect, "color": random_color()})
    bricks.append(row)

# Function to draw bricks
def draw_bricks():
    for row in bricks:
        for brick in row:
            pygame.draw.rect(screen, brick["color"], brick["rect"])

# Function to draw the paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, paddle_width, paddle_height), 0)

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
    if paddle_pos_x > width - paddle_width:
        paddle_pos_x = width - paddle_width

# Ball settings
ball_radius = 20
ball_color = BLUE
ball_pos = [width // 2, height // 2]
angle = random.uniform(30, 150)
speed = random.uniform(7, 11)
velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]

# Frame rate setup
frame_rate = 75  # Adjustable frame rate

def ball_behavior():
    global ball_pos, velocity, running

    # Move the ball
    ball_pos[0] += velocity[0]
    ball_pos[1] += velocity[1]

    # Ball collision detection with the edges
    if ball_pos[0] <= ball_radius or ball_pos[0] >= width - ball_radius:
        velocity[0] = -velocity[0]
    if ball_pos[1] <= ball_radius:
        velocity[1] = -velocity[1]
    if ball_pos[1] >= height - ball_radius:
        running = False  # End game if ball hits the bottom edge

    # Ball collision detection with paddle
    if (paddle_pos_x <= ball_pos[0] <= paddle_pos_x + paddle_width and
            paddle_pos_y - ball_radius <= ball_pos[1] <= paddle_pos_y):
        velocity[1] = -velocity[1]
        ball_pos[1] = paddle_pos_y - ball_radius  # Ensure the ball doesn't get stuck in the paddle

    # Ball collision detection with bricks
    for row in bricks:
        for brick in row:
            if brick["rect"].collidepoint(ball_pos):
                row.remove(brick)
                velocity[1] = -velocity[1]
                break

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    countdown_timer()
    screen.fill(BLACK)
    draw_paddle(paddle_pos_x, paddle_pos_y)
    move_paddle()
    draw_bricks()
    draw_edges()
    ball_behavior()

    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()

    pygame.time.Clock().tick(frame_rate)

# Quit Pygame
pygame.quit()
sys.exit()
