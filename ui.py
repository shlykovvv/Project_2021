import pygame.draw
import pygame
import sys
from constants import WIDTH, HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))

NUMBER_OF_TYPES = 3
NODE_COUNT = 250
SIMULATIONS_PER_FRAME = 2

DRAW_CONNECTIONS = True
type_for_click = 0

color_light = (170, 170, 170)
color_dark = (120, 120, 120)

controllers = {'force': {'x': 70, 'y': 123}, 'radius': {'x': 70, 'y': 153},
               'speed': {'x': 70, 'y': 183}, 'frame': {'x': 70, 'y': 213},
               'connections': True, 'types': {'x': 70, 'y': 295},
               'count': {'x': 70, 'y': 325}, 'brush': 0}


def draw_buttons(mouse):
    if 30 <= mouse[0] <= 250 and 347 <= mouse[1] <= 387:
        pygame.draw.rect(screen, color_light, [30, 347, 220, 40])
    else:
        pygame.draw.rect(screen, color_dark, [30, 347, 220, 40])
    if 30 <= mouse[0] <= 250 and 40 <= mouse[1] <= 80:
        pygame.draw.rect(screen, color_light, [30, 40, 220, 40])
    else:
        pygame.draw.rect(screen, color_dark, [30, 40, 220, 40])


def controllers_info(mouse):
    x, y = mouse[0], mouse[1]
    for s in controllers:
        if s != 'connections' and s != 'brush':
            if controllers[s]['y'] - 3 <= y <= controllers[s]['y'] + 9:
                controllers[s]['x'] = x - 4
        if s == 'connections':
            if 30 <= x <= 50 and 230 <= y <= 250:
                if controllers[s]:
                    controllers[s] = False
                else:
                    controllers[s] = True
    controllers['frame']['x'] = int((controllers['frame']['x'] - 26) / 24) * 24 + 26
    controllers['types']['x'] = int((controllers['types']['x'] - 26) / 27) * 27 + 26


def draw_controllers():
    for s in controllers:
        if s != 'connections' and s != 'brush':
            pygame.draw.rect(screen, (150, 150, 150), [30, controllers[s]['y'], 220, 6])
            pygame.draw.rect(screen, (100, 100, 100), [controllers[s]['x'], controllers[s]['y'] - 3, 8, 12])
        if s == 'connections':
            pygame.draw.rect(screen, color_dark, [30, 230, 20, 20])
            if controllers[s]:
                pygame.draw.polygon(screen, 'white', [(36, 250), (30, 244), (32, 242), (36, 246), (48, 230), (50, 232)])
