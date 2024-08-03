import pygame
import settings

def draw_text(screen, text, position, font_size=30, color=(255, 255, 255)):
    """
    Draws text on the given screen at the specified position.

    Args:
        screen (pygame.Surface): The surface on which the text will be drawn.
        text (str): The text to be drawn.
        position (tuple): The x and y coordinates of the top-left corner of the text.
        font_size (int, optional): The size of the font in pixels. Defaults to 30.
        color (tuple, optional): The RGB color of the text. Defaults to (255, 255, 255).

    Returns:
        None
    """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_score(screen, score):
    """
    Draws the score on the given screen at the top left corner.

    Args:
        screen (pygame.Surface): The surface on which the score will be drawn.
        score (int): The score to be displayed.

    Returns:
        None
    """
    draw_text(screen, f"Score: {score}", (10, 10))

def draw_tries(screen, tries):
    """
    Draws the score on the given screen at the top left corner.

    Args:
        screen (pygame.Surface): The surface on which the score will be drawn.
        score (int): The score to be displayed.

    Returns:
        None
    """
    draw_text(screen, f"Tries: {tries}", (settings.width - 100, 10))

def draw_level(screen, level):
    """
    Draws the level on the given screen at the top left corner.

    Args:
        screen (pygame.Surface): The surface on which the level will be drawn.
        level (int): The level to be displayed.

    Returns:
        None
    """
    draw_text(screen, f"Level: {level}", (settings.width // 2 - 40, 10))

def draw_edges(screen):
    """
    Draws the edges of the game screen.

    This function uses the Pygame library to draw three rectangles on the screen to represent the edges.
    The first rectangle is drawn at the top of the screen with a width equal to the width of the screen and a height of 5 pixels.
    The second rectangle is drawn at the left side of the screen with a width of 5 pixels and a height equal to the height of the screen.
    The third rectangle is drawn at the right side of the screen with a width of 5 pixels and a height equal to the height of the screen.

    Parameters:
    - screen (pygame.Surface): The surface on which the edges will be drawn.

    Returns:
    - None
    """
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, settings.width, 5))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 5, settings.height))
    pygame.draw.rect(screen, (255, 255, 255), (settings.width - 5, 0, 5, settings.height))