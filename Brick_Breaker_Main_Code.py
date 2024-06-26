import pygame
import pygame_menu
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Brick Breaker")

# Colors for the game text
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Frame rate setup
frame_rate = 75  # Adjustable frame rate

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
def generate_bricks():
    bricks = []
    for i in range(brick_rows):
        row = []
        for j in range(brick_columns):
            brick_rect = pygame.Rect(brick_offset_x + j * (brick_width + brick_spacing),
                                     brick_offset_y + i * (brick_height + brick_spacing),
                                     brick_width, brick_height)
            row.append({"rect": brick_rect, "color": random_color()})
        bricks.append(row)
    return bricks

# Function to draw edges of the screen
def draw_edges():
    edge_thickness = 10
    edge_color = (255, 255, 255, 128)  # White with transparency
    pygame.draw.rect(screen, edge_color, (0, 0, edge_thickness, height), 0)
    pygame.draw.rect(screen, edge_color, (width - edge_thickness, 0, edge_thickness, height), 0)
    pygame.draw.rect(screen, edge_color, (0, 0, width, edge_thickness), 0)
    pygame.draw.rect(screen, edge_color, (0, height - edge_thickness, width, edge_thickness), 0)

# Function to draw number of tries on the right-hand side of the screen while the game is running
def draw_tries(tries):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Tries: " + str(tries), True, WHITE)
    screen.blit(text, (width - 300, 20))

# Function to draw the score on the left-hand side of the screen
def draw_score(score):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (20, 20))

# Function to draw bricks
def draw_bricks(bricks):
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
speed = random.uniform(7, 13)
velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]

def ball_behavior():
    global ball_pos, velocity, running, tries, score

    # Bounce off the left and right edges
    if ball_pos[0] - ball_radius <= 0:
        ball_pos[0] = ball_radius
        velocity[0] = -velocity[0]
    elif ball_pos[0] + ball_radius >= width:
        ball_pos[0] = width - ball_radius
        velocity[0] = -velocity[0]

    # Bounce off the top edge
    if ball_pos[1] - ball_radius <= 0:
        ball_pos[1] = ball_radius
        velocity[1] = -velocity[1]

    # Ball falls below the bottom edge
    if ball_pos[1] + ball_radius >= height:
        if tries > 0:
            # Reset ball position
            ball_pos = [width // 2, height // 2]
            angle = random.uniform(30, 150)
            speed = random.uniform(7, 11)
            velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]
            
            # Decrease the number of tries
            tries -= 1
        elif tries == 0:
            running = False
            
            # Display game over screen
            game_over_screen()

    # Ball collision detection with paddle
    if (paddle_pos_x <= ball_pos[0] <= paddle_pos_x + paddle_width and
            paddle_pos_y - ball_radius <= ball_pos[1] <= paddle_pos_y):
        velocity[1] = -velocity[1]
        ball_pos[1] = paddle_pos_y - ball_radius  # Ensures the ball doesn't get stuck in the paddle

    # Ball collision detection with bricks
    for row in bricks:
        for brick in row:
            if brick["rect"].colliderect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, 2 * ball_radius, 2 * ball_radius):
                row.remove(brick)
                score += 10
                velocity[1] = -velocity[1]
                break

def game_over_screen():
    screen.fill(BLACK)
    
    font = pygame.font.SysFont(None, 50)
    texts = ["Game Over", f"Score: {score}", "Press Enter to Restart"]
    y_offset = height // 2 - 100  # Start a bit higher on the screen

    for text in texts:
        rendered_text = font.render(text, True, WHITE)
        text_rect = rendered_text.get_rect(center=(width // 2, y_offset))
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
    global running, tries, score, ball_pos, velocity, bricks

    # Reset tries, score, and ball position
    tries = 3
    score = 0
    ball_pos = [width // 2, height // 2]
    angle = random.uniform(30, 150)
    speed = random.uniform(7, 13)
    velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]

    # Regenerate bricks
    bricks = generate_bricks()

    running = True

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw_score(score)
        draw_tries(tries)
        draw_paddle(paddle_pos_x, paddle_pos_y)
        move_paddle()
        draw_bricks(bricks)
        draw_edges()
        ball_behavior()

        # Update ball position
        ball_pos[0] += velocity[0]
        ball_pos[1] += velocity[1]

        pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
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
