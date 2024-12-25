import pygame
import random
import settings  # Import settings for screen width and height

class Ball:
    def __init__(self, x, y, radius):
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.color = (0, 0, 255)  # Blue
        self.speed = 5
        self.direction = [0, -1]  # Start moving upwards
        self.attached = True

    def move(self, bricks):
        """
        Moves the ball and checks for collisions with walls and bricks.

        Args:
            bricks (list): List of Brick objects.
        """
        if not self.attached:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed

            # Bounce off walls
            if self.rect.left <= 0 or self.rect.right >= settings.width:
                self.direction[0] *= -1
            if self.rect.top <= 0:
                self.direction[1] *= -1

            # Check for brick collision
            self.handle_brick_collision(bricks)

    def handle_brick_collision(self, bricks):
        """
        Handles ball collision with bricks and adjusts its direction.

        Args:
            bricks (list): List of Brick objects.
        """
        for brick in bricks[:]:
            if self.rect.colliderect(brick.rect):
                # Determine collision side
                overlap_x = min(self.rect.right - brick.rect.left, brick.rect.right - self.rect.left)
                overlap_y = min(self.rect.bottom - brick.rect.top, brick.rect.bottom - self.rect.top)

                if overlap_x < overlap_y:
                    # Horizontal collision
                    self.direction[0] *= -1
                else:
                    # Vertical collision
                    self.direction[1] *= -1

                # Remove the brick
                bricks.remove(brick)
                break

    def launch(self):
        """
        Launches the ball upwards when spacebar is pressed.
        """
        if self.attached:
            self.attached = False
            self.direction = [0, -1]  # Straight up

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def reset(self, paddle):
        """
        Resets the ball position and state.

        Args:
            paddle (Paddle): The paddle object.
        """
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top
        self.attached = True
        self.direction = [0, -1]

class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < settings.width:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
