import pygame.draw
import pygame
import sys
from view import w, h, screen


NUMBER_OF_TYPES = 3  # TODO: добавить контроллер-scrollbar
NODE_COUNT = 250  # TODO: добавить контроллер-scrollbar
SIMULATIONS_PER_FRAME = 2  # TODO: добавить контроллер-scrollbar

DRAW_CONNECTIONS = True  # TODO: добавить галочку
type_for_click = 0  # TODO: заготовочка под выбор типа частицы для создания по клику

color_light = (250, 250, 250)
color_dark = (170, 170, 170)


def create_button():
    global text
    smallfont = pygame.font.SysFont('Corbel', int(w / 40))
    text = smallfont.render('Create new world', True, (0, 0, 0))  # TODO: сделать кнопку красивой


def draw_button(mouse):
    if mouse[0] >= w and mouse[1] <= h / 5:
        pygame.draw.rect(screen, color_light, [w, 0, w + 150, h / 5])
    else:
        pygame.draw.rect(screen, color_dark, [w, 0, w + 150, h / 5])
    screen.blit(text, (w + 20, h / 10 - 5))