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

#edges of the screen be hard coded and nothing can pass through them at all costs (they are invisible)
def edges():
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 10, height), 0)
    pygame.draw.rect(screen, (255, 255, 255), (width - 10, 0, 10, height), 0)
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, width, 10), 0)
    pygame.draw.rect(screen, (255, 255, 255), (0, height - 10, width, 10), 0)

#Paddle Setting values
paddle_width = 400
paddle_length = 100
paddle_pos_y = height - 100
paddle_pos_x = width // 2 - paddle_width // 2

# Function to draw the paddle
def paddle(x, y):
    pygame.draw.rect(screen, (255, 255, 255), (x, y, paddle_width, paddle_length), 0)

# Ball settings
ball_radius = 20
ball_color = (0, 0, 255)
ball_pos = [width // 2, height // 2]
angle = random.uniform(20, 160)
speed = random.uniform(7, 11)
velocity = [speed * math.cos(math.radians(angle)), speed * math.sin(math.radians(angle))]

# Frame rate setup
frame_rate = 75  # Adjustable frame rate

def ball_behavior():
    global ball_pos, velocity
    running = True
    while running:
            # Move the ball with gravity effect
            ball_pos[0] += int(velocity[0])
            ball_pos[1] += int(velocity[1])
  
            # Collision detection with the edges
            if ball_pos[0] <= ball_radius or ball_pos[0] >= width - ball_radius:
                velocity[0] = -velocity[0]
            if ball_pos[1] <= ball_radius or ball_pos[1] >= height - ball_radius:
                velocity[1] = -velocity[1]
            
            # Collision detection with the paddle
            if ball_pos[1] >= paddle_pos_y - ball_radius and ball_pos[1] <= paddle_pos_y + paddle_length + ball_radius:
                if ball_pos[0] >= paddle_pos_x - ball_radius and ball_pos[0] <= paddle_pos_x + paddle_width + ball_radius:
                    velocity[1] = -velocity[1]

#created thread for ball behavior
ball_thread = threading.Thread(target=ball_behavior)

# Main loop
running = True
while running:

    # Update the screen
    pygame.display.update()

    # Limit the frame rate
    pygame.time.Clock().tick(frame_rate)
   
    #exit pgygame if the window is closed
    if not pygame.display.get_init():
        running = False

# Quit Pygame 
pygame.quit()
sys.exit()
