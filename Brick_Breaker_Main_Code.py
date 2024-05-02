import pygame
import sys
import threading

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))

# Ball settings
ball_pos = [width // 960, height // 540]
ball_radius = 14
ball_color = (255, 0, 0)
velocity = [2, 2]  # X and Y velocity
gravity = 0.1
energy_loss_factor = 0.9  # Energy loss on bouncing

# Frame rate setup
frame_rate = 75
clock = pygame.time.Clock()

# Lock for thread-safe operations on ball_pos
position_lock = threading.Lock()

def ball_behavior():
    global ball_pos, velocity
    running = True
    while running:
        with position_lock:
            # Move the ball
            ball_pos[0] += velocity[0]
            ball_pos[1] += velocity[1]

            # Gravity effect
            velocity[1] += gravity

            # Collision detection with the walls
            if ball_pos[0] <= ball_radius or ball_pos[0] >= width - ball_radius:
                velocity[0] = -velocity[0] * energy_loss_factor
                ball_pos[0] = ball_radius if ball_pos[0] < ball_radius else width - ball_radius
            
            if ball_pos[1] <= ball_radius or ball_pos[1] >= height - ball_radius:
                velocity[1] = -velocity[1] * energy_loss_factor
                ball_pos[1] = ball_radius if ball_pos[1] < ball_radius else height - ball_radius

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

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw the ball
    with position_lock:
        pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)

    # Update the display
    pygame.display.flip()

    # Frame rate control
    clock.tick(frame_rate)

pygame.quit()
sys.exit()
