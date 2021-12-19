import pygame
import sys
from constants import WIDTH, HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))

NUMBER_OF_TYPES = 2
NODE_COUNT = 250
SIMULATIONS_PER_FRAME = 2

NODE_RADIUS = 5
LINK_FORCE = - 0.015
SPEED = 4

type_for_click = 0

color_light = (170, 170, 170)
color_dark = (120, 120, 120)

controllers = {'force': {'x': 26 - (LINK_FORCE / 0.04) * 220, 'y': 123},
               'radius': {'x': 26 + ((NODE_RADIUS - 3) / 7) * 220, 'y': 153},
               'speed': {'x': 26 + (SPEED / 40) * 220, 'y': 183},
               'frame': {'x': 26 + (SIMULATIONS_PER_FRAME - 1) * 24, 'y': 213},
               'types': {'x': 26 + (NUMBER_OF_TYPES - 1) * 27, 'y': 295},
               'count': {'x': 26 + (NODE_COUNT / 300) * 220, 'y': 325},
               'connections': True, 'brush': 0}


def change_controllers(mouse):
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
    controllers['frame']['x'] = ((controllers['frame']['x'] - 26) // 24) * 24 + 26
    controllers['types']['x'] = int((controllers['types']['x'] - 26) / 27) * 27 + 26


def change_characteristics():
    global NODE_COUNT, LINK_FORCE, NODE_RADIUS, SPEED, SIMULATIONS_PER_FRAME
    LINK_FORCE = - int((controllers['force']['x'] - 26) / 220 * 40) / 1000
    NODE_COUNT = int((controllers['count']['x'] - 26) / 220 * 300)
    NODE_RADIUS = int(300 + (controllers['radius']['x'] - 26) / 220 * 700) / 100
    SPEED = int((controllers['speed']['x'] - 26) / 220 * 400) / 10
    SIMULATIONS_PER_FRAME = int(1 + (controllers['frame']['x'] - 2) / 220 * 9)
