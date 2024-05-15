import pygame
import sys
import threading
import random
import math

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)

# Screen dimensions and settings
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Brick Breaker")

# Frame rate setup
frame_rate = 75  # Adjustable frame rate

# Ball settings
ball_radius = 20
ball_color = (0, 0, 255)
ball_pos = [width // 2, height // 2]
angle = random.uniform(20, 160)
speed = random.uniform(7, 11)
velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]

#Paddle Setting values
paddle_width = 400
paddle_length = 100
paddle_pos_y = height - 50

#paddle x position
paddle_pos_x = width // 2 - paddle_width // 2


# Lock for thread-safe operations on ball_pos
position_lock = threading.Lock()

def ball_behavior():
    global ball_pos, velocity
    running = True
    while running:
        with position_lock:
            # Move the ball
            ball_pos[0] += int(velocity[0])
            ball_pos[1] += int(velocity[1])

            # Gravity effect (if applicable)
            # velocity[1] += gravity (This can be adjusted based on game physics needs)

            # Wall bounce
            if ball_pos[0] <= ball_radius or ball_pos[0] >= width - ball_radius:
                velocity[0] = -velocity[0]
            if ball_pos[1] <= ball_radius or ball_pos[1] >= height - ball_radius:
                velocity[1] = -velocity[1]
                
            # Collision detection with the walls, ball can't pass through walls
            if ball_pos[0] <= ball_radius or ball_pos[0] >= width - ball_radius:
                velocity[0] = -velocity[0]
            if ball_pos[1] <= ball_radius or ball_pos[1] >= height - ball_radius:
                velocity[1] = -velocity[1]

            # Collision detection with the paddle
            if ball_pos[1] >= paddle_pos_y - ball_radius and ball_pos[1] <= paddle_pos_y + paddle_length + ball_radius:
                if ball_pos[0] >= paddle_pos_x - ball_radius and ball_pos[0] <= paddle_pos_x + paddle_width + ball_radius:
                    velocity[1] = -velocity[1]

        # Simulate frame rate for the thread
        pygame.time.wait(int(1000 / frame_rate))

# Thread for ball movement
ball_thread = threading.Thread(target=ball_behavior)
ball_thread.start()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            ball_thread.join()  # Ensure thread is cleaned up on quit

    screen.fill((0, 0, 0))

    # Draw the ball
    with position_lock:
        pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)
        pygame.draw.rect(screen, (255, 255, 255), (paddle_pos_x, paddle_pos_y, paddle_width, paddle_length), 0)
        translucent_surface = pygame.Surface((paddle_length, paddle_width), pygame.SRCALPHA)
        translucent_surface.fill((*BLACK, 25))
        screen.blit(translucent_surface, (paddle_pos_x, paddle_pos_y))

   
    pygame.display.flip()
    pygame.time.Clock().tick(frame_rate)

     # Update the display
    pygame.display.update()

pygame.quit()
sys.exit()
