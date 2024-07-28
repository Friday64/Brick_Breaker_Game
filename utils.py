import pygame
import settings

def draw_text(screen, text, position, font_size=30, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_score(screen, score):
    draw_text(screen, f"Score: {score}", (10, 10))

def draw_tries(screen, tries):
    draw_text(screen, f"Tries: {tries}", (settings.width - 100, 10))

def draw_level(screen, level):
    draw_text(screen, f"Level: {level}", (settings.width // 2 - 40, 10))

def draw_edges(screen):
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, settings.width, 5))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 5, settings.height))
    pygame.draw.rect(screen, (255, 255, 255), (settings.width - 5, 0, 5, settings.height))