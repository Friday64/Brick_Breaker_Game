import random
import pygame
import settings

class Powerup:
    def __init__(self, x, y, color, effect):
        """
        Initializes a Powerup object.

        Args:
            x (int): The x-coordinate of the top-left corner of the powerup.
            y (int): The y-coordinate of the top-left corner of the powerup.
            color (tuple): The RGB color of the powerup.
            effect (function): The function that defines the effect of the powerup.

        Returns:
            None
        """
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.effect = effect
        self.speed = 2

    def move(self):
        """
        Move the Powerup object vertically by updating its rect's y-coordinate.

        This method increments the y-coordinate of the Powerup object's rect by the value of its speed attribute.

        Parameters:
            self (Powerup): The Powerup object.

        Returns:
            None
        """
        self.rect.y += self.speed

    def draw(self, screen):
        """
        Draws a rectangle on the given screen using the specified color and rectangular coordinates.

        Parameters:
            screen (pygame.Surface): The screen on which the rectangle will be drawn.

        Returns:
            None
        """
        pygame.draw.rect(screen, self.color, self.rect)

def generate_powerup():
    """
    Generates a random powerup object.

    This function generates a random powerup object with a random x-coordinate within the range of 0 to the width of the game screen minus 20. The powerup type is randomly chosen from the list ['multiball', 'paddle_size', 'slow_ball']. Depending on the chosen powerup type, a Powerup object is created with the corresponding color and effect.

    Returns:
        Powerup: A Powerup object with a random x-coordinate, a y-coordinate of 0, a color, and an effect.

    """
    x = random.randint(0, settings.width - 20)
    powerup_type = random.choice(['multiball', 'paddle_size', 'slow_ball'])
    if powerup_type == 'multiball':
        return Powerup(x, 0, (0, 255, 0), 'multiball')  # Green
    elif powerup_type == 'paddle_size':
        return Powerup(x, 0, (255, 255, 0), 'paddle_size')  # Yellow
    else:
        return Powerup(x, 0, (128, 0, 128), 'slow_ball')  # Purple

def handle_powerups(powerups, paddle, balls):
    """
    Handle the powerups in the game.

    Args:
        powerups (List[Powerup]): The list of powerups in the game.
        paddle (Paddle): The paddle object.
        balls (List[Ball]): The list of balls in the game.

    Returns:
        None

    This function iterates over the powerups in the game and performs the following actions:
    1. Move each powerup.
    2. Check if the powerup collides with the paddle.
    3. If the powerup collides with the paddle:
        - If the powerup has the 'multiball' effect, create a new ball and add it to the list of balls.
        - If the powerup has the 'paddle_size' effect, increase the width of the paddle.
        - If the powerup has the 'slow_ball' effect, decrease the speed of each ball.
    4. Remove the powerup from the list.
    5. If the powerup is no longer visible on the screen, remove it from the list.

    Note:
    - The function modifies the powerups, paddle, and balls objects.
    - The function does not return any value.
    """
    for powerup in powerups[:]:
        powerup.move()
        if powerup.rect.colliderect(paddle.rect):
            if powerup.effect == 'multiball':
                new_ball = Ball(balls[0].rect.centerx, balls[0].rect.centery, settings.ball_radius)
                new_ball.attached = False
                new_ball.direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
                balls.append(new_ball)
            elif powerup.effect == 'paddle_size':
                paddle.rect.width = min(paddle.rect.width * 1.5, settings.width)
            elif powerup.effect == 'slow_ball':
                for ball in balls:
                    ball.speed = max(ball.speed * 0.5, 1)
            powerups.remove(powerup)
        elif powerup.rect.top > settings.height:
            powerups.remove(powerup)