import pygame
import random
import settings

class Ball:
    def __init__(self, x, y, radius):
        """
        Initializes a new instance of the Ball class.

        Args:
            x (int): The x-coordinate of the center of the ball.
            y (int): The y-coordinate of the center of the ball.
            radius (int): The radius of the ball.

        Returns:
            None

        Initializes the following instance variables:
            - radius (int): The radius of the ball.
            - rect (pygame.Rect): The rectangle representing the ball's position and size.
            - color (tuple): The color of the ball as an RGB tuple.
            - speed (int): The speed of the ball.
            - direction (list): The direction of the ball as a list of x and y components.
            - attached (bool): A flag indicating whether the ball is attached or not.
        """
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.color = (0, 0, 255)  # Blue
        self.speed = 5
        self.direction = [0, -1]  # Start moving upwards
        self.attached = True

    def move(self):
        """
        Moves the ball based on the current direction and speed.

        Returns:
            None
        """
        if not self.attached:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed

            if self.rect.left <= 0 or self.rect.right >= settings.width:
                self.direction[0] *= -1
            if self.rect.top <= 0:
                self.direction[1] *= -1

    def draw(self, screen):
        """
        Draws a circle on the given screen using the specified color and radius.

        Parameters:
            screen (pygame.Surface): The screen on which the circle will be drawn.

        Returns:
            None
        """
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def reset(self, paddle):
        """
        Resets the position and properties of the Ball object.

        Args:
            paddle (Paddle): The Paddle object to which the Ball is attached.

        Returns:
            None

        This function resets the position of the Ball object to the center of the given Paddle object and sets its bottom position to the top of the Paddle. It also sets the attached flag to True and the direction to [0, -1], which means the Ball will start moving upwards.
        """
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top
        self.attached = True
        self.direction = [0, -1]

class Paddle:
    """
        Initializes a new instance of the class.

        Args:
            x (int): The x-coordinate of the top-left corner of the rectangle.
            y (int): The y-coordinate of the top-left corner of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.

        Returns:
            None

        Initializes the following instance variables:
            - rect (pygame.Rect): The rectangle representing the position and size of the object.
            - color (tuple): The color of the object as an RGB tuple.
            - speed (int): The speed of the object.
    """
    def __init__(self, x, y, width, height):
        """
        Initializes a new instance of the class.

        Args:
            x (int): The x-coordinate of the top-left corner of the rectangle.
            y (int): The y-coordinate of the top-left corner of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.

        Initializes the following instance variables:
            - rect (pygame.Rect): The rectangle representing the position and size of the object.
            - color (tuple): The color of the object as an RGB tuple.
            - speed (int): The speed of the object.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White
        self.speed = 5

    def move(self, keys):
        """
        Move the object horizontally based on the keys pressed.

        Args:
            keys (dict): A dictionary containing the keys pressed by the user.

        Returns:
            None

        This method moves the object horizontally based on the keys pressed. If the left arrow key is pressed and the object is not at the leftmost position, the object moves left by the speed. If the right arrow key is pressed and the object is not at the rightmost position, the object moves right by the speed.
        """
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < settings.width:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Brick:
    def __init__(self, x, y, width, height):
        """
        Initializes a new instance of the class.

        Args:
            x (int): The x-coordinate of the top-left corner of the rectangle.
            y (int): The y-coordinate of the top-left corner of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.

        Initializes the following instance variables:
            - rect (pygame.Rect): The rectangle representing the position and size of the object.
            - color (tuple): The color of the object as an RGB tuple.

        Generates a random RGB color for the object's color attribute.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def draw(self, screen):
        """
        Initializes a new instance of the class.

        Args:
            x (int): The x-coordinate of the top-left corner of the rectangle.
            y (int): The y-coordinate of the top-left corner of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.

        Initializes the following instance variables:
            - rect (pygame.Rect): The rectangle representing the position and size of the object.
            - color (tuple): The color of the object as an RGB tuple.

        Generates a random RGB color for the object's color attribute.
        """
        pygame.draw.rect(screen, self.color, self.rect)