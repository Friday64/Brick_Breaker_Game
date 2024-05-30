import pygame
import sys
import threading
import random
import math

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Screen dimensions and settings
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Brick Breaker")

# Edges of the screen
def draw_edges():
    pygame.draw.rect(screen, WHITE, (0, 0, 10, height), 0)
    pygame.draw.rect(screen, WHITE, (width - 10, 0, 10, height), 0)
    pygame.draw.rect(screen, WHITE, (0, 0, width, 10), 0)
    pygame.draw.rect(screen, WHITE, (0, height - 10, width, 10), 0)

# Paddle settings
paddle_width = 400
paddle_height = 20
paddle_pos_y = height - 100
paddle_pos_x = width
paddle_speed = 10 

#brick settings
brick_rows = 5
brick_columns = 10
brick_width = 100
brick_height = 50
brick_spacing = 10
brick_offset_x = (width - (brick_columns * (brick_width + brick_spacing))) // 2
brick_offset_y = 50

#function to draw bricks on a grid of configured size
def draw_brick(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, 100, 50), 0)

#empty array to store bricks, bricks_pos_x and bricks_pos_y are arrays of arrays
bricks = []
bricks_pos_x = []
bricks_pos_y = []
for i in range(brick_rows):
    bricks.append([])
    bricks_pos_x.append([])
    bricks_pos_y.append([])
    for j in range(brick_columns):
        bricks[i].append(1)
        bricks_pos_x[i].append(brick_offset_x + j * (brick_width + brick_spacing))
        bricks_pos_y[i].append(brick_offset_y + i * (brick_height + brick_spacing))

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
angle = random.uniform(20, 160)
speed = random.uniform(7, 11)
velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]

# Frame rate setup
frame_rate = 75  # Adjustable frame rate

def ball_behavior():
    global ball_pos, velocity, running
    while running:
        # Move the ball
        ball_pos[0] += velocity[0]
        ball_pos[1] += velocity[1]
  
        # ball Collision detection with the edges
        if ball_pos[0] <= 0 or ball_pos[0] >= width - ball_radius:
            velocity[0] = -velocity[0]
        if ball_pos[1] <= 0 or ball_pos[1] >= height - ball_radius:
            velocity[1] = -velocity[1]
       
        # ball Collision detection with paddle
        if ball_pos[0] >= paddle_pos_x and ball_pos[0] <= paddle_pos_x + paddle_width and ball_pos[1] >= paddle_pos_y and ball_pos[1] <= paddle_pos_y + paddle_height:
            velocity[1] = -velocity[1]

        # ball Collision detection with bricks
        for i in range(brick_rows):
            for j in range(brick_columns):
                if bricks[i][j] == 1:
                    if ball_pos[0] >= bricks_pos_x[i][j] and ball_pos[0] <= bricks_pos_x[i][j] + brick_width and ball_pos[1] >= bricks_pos_y[i][j] and ball_pos[1] <= bricks_pos_y[i][j] + brick_height:
                        bricks[i][j] = 0
                        velocity[1] = -velocity[1]

        # Limit the frame rate
        pygame.time.Clock().tick(frame_rate)

# Start the ball behavior thread
running = True
ball_thread = threading.Thread(target=ball_behavior)
ball_thread.start()

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]or keys[pygame.K_a]:
        paddle_pos_x -= 10
    if keys[pygame.K_RIGHT]or keys[pygame.K_d]:
        paddle_pos_x += 10

    # Make sure the paddle doesn't go off screen
    if paddle_pos_x < 0:
        paddle_pos_x = 0
    if paddle_pos_x > width - paddle_width:
        paddle_pos_x = width - paddle_width

    # Fill the screen with black
    screen.fill(BLACK)

    # Draw edges
    draw_edges()
    
    #for loop to draw set of bricks within the grid
    for i in range(brick_rows):
        for j in range(brick_columns):
            if bricks[i][j] == 1:
                draw_brick(bricks_pos_x[i][j], bricks_pos_y[i][j])

    
    # Draw paddle and ball
    draw_paddle(paddle_pos_x, paddle_pos_y)
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    pygame.time.Clock().tick(frame_rate)

# Quit Pygame and exit the thread
running = False
ball_thread.join()
pygame.quit()
sys.exit()
