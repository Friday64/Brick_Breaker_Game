import pygame
import pygame_menu
import game
import settings

def menu():
    """Display the game menu."""
    pygame.init()
    screen = pygame.display.set_mode((settings.width, settings.height), pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("Brick Breaker")
    
    menu = pygame_menu.Menu('Brick Breaker', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', game.start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

if __name__ == "__main__":
    menu()