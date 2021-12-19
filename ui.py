import pygame
from constants import WIDTH, HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))

"""main parameters"""
NUMBER_OF_TYPES = 3
NODE_COUNT = 250
SIMULATIONS_PER_FRAME = 2
NODE_RADIUS = 5
LINK_FORCE = - 0.015
SPEED = 4

color_light = (170, 170, 170)
color_dark = (120, 120, 120)

"""info about all controllers like sliders, buttons, etc."""
controllers = {'force': {'x': 26 - (LINK_FORCE / 0.04) * 220, 'y': 123},
               'radius': {'x': 26 + ((NODE_RADIUS - 3) / 7) * 220, 'y': 153},
               'speed': {'x': 26 + (SPEED / 40) * 220, 'y': 183},
               'frame': {'x': 26 + (SIMULATIONS_PER_FRAME - 1) * 24, 'y': 213},
               'types': {'x': 26 + (NUMBER_OF_TYPES - 1) * 27, 'y': 295},
               'count': {'x': 26 + (NODE_COUNT / 450) * 220, 'y': 325},
               'connections': True, 'brush': 0}


def change_controllers(mouse):
    """this function changes the parameters of 'controllers' using mouse's coordinates"""
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
        if s == 'brush' and 420 <= y <= 460:
            controllers[s] = int((x - 30) / 220 * NUMBER_OF_TYPES)
    controllers['frame']['x'] = int((controllers['frame']['x'] - 26) / 24) * 24 + 26
    controllers['types']['x'] = int((controllers['types']['x'] - 26) / 27) * 27 + 26


def change_characteristics():
    """this function changes values of main parameters using sliders' positions"""
    global NODE_COUNT, LINK_FORCE, NODE_RADIUS, SPEED, SIMULATIONS_PER_FRAME, NUMBER_OF_TYPES
    LINK_FORCE = - int((controllers['force']['x'] - 26) / 220 * 40) / 1000
    NODE_COUNT = int((controllers['count']['x'] - 26) / 220 * 450)
    NODE_RADIUS = int(300 + (controllers['radius']['x'] - 26) / 220 * 700) / 100
    SPEED = int((controllers['speed']['x'] - 26) / 220 * 400) / 10
    SIMULATIONS_PER_FRAME = int(1 + (controllers['frame']['x'] - 2) / 220 * 9)
    NUMBER_OF_TYPES = int(1 + (controllers['types']['x'] - 2) / 220 * 8)


def read_laws_from_file(input_filename):
    """this functions reads laws of the world from a certain file"""
    with open(input_filename, 'r') as input_file:
        i = 0
        lines_conv = [0] * 50
        for line in input_file:
            lines_conv[i] = line.split(',')
            for j in range(len(lines_conv[i])):
                lines_conv[i][j] = int(lines_conv[i][j])
            i += 1
        links_possible, coupling = [0] * len(lines_conv[0]), [0] * len(lines_conv[0])
        for k in range(len(lines_conv[0])):
            links_possible[k] = lines_conv[k + 1]
            coupling[k] = lines_conv[k + len(lines_conv[0]) + 1]
        return lines_conv[0], links_possible, coupling, len(lines_conv[0])


def write_laws_to_file(output_filename, links, links_possible, coupling):
    """this function wtites laws of the world to a certain file"""
    with open(output_filename, 'w') as out_file:
        for i in range(len(links)):
            out_file.write(str(links[i]))
            if i < len(links) - 1:
                out_file.write(',')
        for i in range(len(links)):
            out_file.write("\n")
            for j in range(len(links)):
                out_file.write(str(links_possible[i][j]))
                if j < len(links) - 1:
                    out_file.write(',')
        for i in range(len(links)):
            out_file.write("\n")
            for j in range(len(links)):
                out_file.write(str(coupling[i][j]))
                if j < len(links) - 1:
                    out_file.write(',')
