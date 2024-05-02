import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))

# Ball settings
ball_pos = [width // 100, height // 100]
ball_radius = 10
ball_color = (0, 0, 255)
velocity = [.8, .8]  # X and Y velocity
gravity = .4
energy_loss_factor = .99  # Energy loss on bouncing

# Clock to control the frame rate
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw the ball
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(75)

pygame.quit()
sys.exit()
