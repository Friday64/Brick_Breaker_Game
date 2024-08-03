import pygame
import pygame_menu
import game
import settings

def main():
    """
    Initializes the Pygame library, sets up the game surface, creates a Pygame-Menu with a "Play" button to start the game and a "Quit" button to exit the game, and starts the main loop of the Pygame-Menu.

    Parameters:
    None

    Returns:
    None
    """
    pygame.init()
    surface = pygame.display.set_mode((settings.width, settings.height))
    pygame.display.set_caption("Brick Breaker")

    menu = pygame_menu.Menu('Brick Breaker', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', game.start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)

if __name__ == "__main__":
    main()