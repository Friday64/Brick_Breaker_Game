import pygame
import pygame_menu
import game
import settings

def main():
    pygame.init()
    surface = pygame.display.set_mode((settings.width, settings.height))
    pygame.display.set_caption("Brick Breaker")

    menu = pygame_menu.Menu('Brick Breaker', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', game.start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)

if __name__ == "__main__":
    main()