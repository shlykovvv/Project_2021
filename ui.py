import pygame.draw
import pygame
import sys
from constants import WIDTH, HEIGHT


screen = pygame.display.set_mode((WIDTH + 150, HEIGHT))  # TODO: допокно для кнопок и регуляторов, нужно его улучшить и сделать красивым

NUMBER_OF_TYPES = 3  # TODO: добавить контроллер-scrollbar
NODE_COUNT = 250  # TODO: добавить контроллер-scrollbar
SIMULATIONS_PER_FRAME = 2  # TODO: добавить контроллер-scrollbar

DRAW_CONNECTIONS = True  # TODO: добавить галочку
type_for_click = 0  # TODO: заготовочка под выбор типа частицы для создания по клику

color_light = (250, 250, 250)
color_dark = (170, 170, 170)
text = ''


def create_button():
    global text
    smallfont = pygame.font.SysFont('Corbel', int(WIDTH / 40))
    text = smallfont.render('Create new world', True, (0, 0, 0))  # TODO: сделать кнопку красивой


def draw_button(mouse):
    if mouse[0] >= WIDTH and mouse[1] <= HEIGHT / 5:
        pygame.draw.rect(screen, color_light, [WIDTH, 0, WIDTH + 150, HEIGHT / 5])
    else:
        pygame.draw.rect(screen, color_dark, [WIDTH, 0, WIDTH + 150, HEIGHT / 5])
    screen.blit(text, (WIDTH + 20, HEIGHT / 10 - 5))
